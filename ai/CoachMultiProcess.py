# Coach.py, but faster
import logging
import coloredlogs
import os
import sys
from collections import deque
from random import shuffle
from multiprocessing import Pool, dummy
import numpy as np
from tqdm import tqdm
from gomoku import GomokuGame
from Arena import Arena
from MCTS import MCTS
from gomokuNNet import NNetWrapper as nn
from utils import dotdict

NUMBER_OF_CORES = os.cpu_count()

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  #

args1 = dotdict({
    'numIters': 10,#20,
    'numEps': 40,#100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 90000, #200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 20, #25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 20, #40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 3,
    'timeLimit' :4.9, 

    'checkpoint': './tests/big_i10e40s20a20_1/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})
args = dotdict({
    'numIters': 3,#20,
    'numEps': 2,#100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 90000, #200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 2, #25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 1, #40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 3,
    'timeLimit' :4.9, 

    'checkpoint': './tests/arenaCompare1/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})
game = GomokuGame(15)
nnet = nn(game)
mcts = MCTS(game, nnet, args)

def executeEpisode(_):
        mcts = MCTS(game, nnet, args)
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
        ---------
            trainExamples: a list of examples of the form (canonicalBoard, currPlayer, pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        print('X', end='', flush=True)#, flush=True)#, end='') 
        trainExamples = []
        board = game.getInitBoard()
        curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard = game.getCanonicalForm(board, curPlayer)
            temp = int(episodeStep < args.tempThreshold)
            print('pi')
            pi = mcts.getActionProb(canonicalBoard, temp=temp)
            print('sym')
            sym = game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            board, curPlayer = game.getNextState(board, curPlayer, action)

            r = game.getGameEnded(board, curPlayer)

            if r != 0:
                return [(x[0], x[2], r * ((-1) ** (x[1] != curPlayer))) for x in trainExamples]
        #print('O', end='', flush=True)

def playGame(player1, player2, game, display, verbose=False):
        """
        Executes one episode of a game.

        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [player2, None, player1]
        curPlayer = 1
        board = game.getInitBoard()
        it = 0
        while game.getGameEnded(board, curPlayer) == 0:
            print(f'interation: {it}')
            it += 1
            if verbose:
                assert display
                #print("Turn ", str(it), "Player ", str(curPlayer))
                log.info(f'Turn {str(it)} Player {str(curPlayer)}')
                display(board)
          #  print('Getting action')
            action = players[curPlayer + 1](game.getCanonicalForm(board, curPlayer))

            valids = game.getValidMoves(game.getCanonicalForm(board, curPlayer), 1)

            if valids[action] == 0:
                log.error(f'Action {action} is not valid!')
                log.debug(f'valids = {valids}')
                assert valids[action] > 0
            board, curPlayer = game.getNextState(board, curPlayer, action)
        if verbose:
            assert display
            #print("Game over: Turn ", str(it), "Result ", str(game.getGameEnded(board, 1)))
            log.info(f'Game over: Turn {str(it)} Result {str(game.getGameEnded(board, 1))}')
            display(board)
        return curPlayer * game.getGameEnded(board, curPlayer)

def getCheckpointFile(self, iteration):
    return 'checkpoint_' + str(iteration) + '.pth.tar'
def zero(_):
    return 43
if __name__ == "__main__":
    log.info('Loading GomokuGame...')
    #game = GomokuGame(15)

    log.info('Loading %s...', nn.__name__)
    nnet = nn(game)
    pnet = nnet.__class__(game)

    mcts = MCTS(game, nnet, args)

    if args.load_model:
        log.info('Loading checkpoint "%s/%s"...', args.load_folder_file)
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')

    trainExamplesHistory = []  # history of examples from args.numItersForTrainExamplesHistory latest iterations
    skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    for i in range(1, args.numIters + 1):
        # bookkeeping
        log.info(f'Starting Iter #{i}/{args.numIters} ...')
        # examples of the iteration
        if not skipFirstSelfPlay or i > 1:
            iterationTrainExamples = deque([], maxlen=args.maxlenOfQueue)
            # iterations
            # tmp =  [MCTS(game, nnet, args) for i in range(args.numEps)]
            
            # Multithreading: 
            # with dummy.Pool() as p:
            def executeEpisodeT(_):
                mcts = MCTS(game, nnet, args)
                print('X', end='', flush=True)#, flush=True)#, end='') 
                trainExamples = []
                board = game.getInitBoard()
                curPlayer = 1
                episodeStep = 0

                while True:
                    episodeStep += 1
                    canonicalBoard = game.getCanonicalForm(board, curPlayer)
                    temp = int(episodeStep < args.tempThreshold)
                    print('pi')
                    pi = mcts.getActionProb(canonicalBoard, temp=temp)
                    print('sym')
                    sym = game.getSymmetries(canonicalBoard, pi)
                    for b, p in sym:
                        trainExamples.append([b, curPlayer, p, None])

                    action = np.random.choice(len(pi), p=pi)
                    board, curPlayer = game.getNextState(board, curPlayer, action)

                    r = game.getGameEnded(board, curPlayer)

                    if r != 0:
                        return [(x[0], x[2], r * ((-1) ** (x[1] != curPlayer))) for x in trainExamples]


            with Pool(NUMBER_OF_CORES) as p:
                # logging.info('we in pool bojs')
                raw = p.map(executeEpisodeT,range(args.numEps))
            iterationTrainExamples = deque(raw)
            logging.info('pool finished')
            # for _ in tqdm(range(args.numEps), desc="Self Play"):
            #     mcts = MCTS(game, nnet, args)  # reset search tree
            #     iterationTrainExamples += executeEpisode()

            # save the iteration examples to the history 
            trainExamplesHistory.append(iterationTrainExamples)

        if len(trainExamplesHistory) > args.numItersForTrainExamplesHistory:
            log.warning(
                f"Removing the oldest entry in trainExamples. len(trainExamplesHistory) = {len(trainExamplesHistory)}")
            trainExamplesHistory.pop(0)
        # backup history to a file
        # NB! the examples were collected using the model from the previous iteration, so (i-1)  
        #TODO 
        # saveTrainExamples(i - 1)

        # shuffle examples before training
        trainExamples = []
        for e in trainExamplesHistory:
            trainExamples.extend(e)
        shuffle(trainExamples)

        # training new network, keeping a copy of the old one
        nnet.save_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
        pnet.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
        pmcts = MCTS(game, pnet, args)

        nnet.train(trainExamples)
        nmcts = MCTS(game, nnet, args)

        log.info('PITTING AGAINST PREVIOUS VERSION')
        arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                        lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), game)
        pwins, nwins, draws = arena.playGames(args.arenaCompare)

        log.info('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
        if pwins + nwins == 0 or float(nwins) / (pwins + nwins) < args.updateThreshold:
            log.info('REJECTING NEW MODEL')
            nnet.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
        else:
            log.info('ACCEPTING NEW MODEL')
            nnet.save_checkpoint(folder=args.checkpoint, filename=getCheckpointFile(i))
            nnet.save_checkpoint(folder=args.checkpoint, filename='best.pth.tar')
        # log.info('PITTING AGAINST PREVIOUS VERSION')
# 
        # arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
        #                 lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), game, display=game.display)
        # 
        # 
        # oneWon_arena = 0
        # twoWon_arena = 0
        # draws_arena = 0
        # log.info('Starting arena compare..')
        # def f(nn):
        #     game_cpy = GomokuGame(15)
        #     nnet = nn[0]
        #     pnet = nn[1]
        #    # arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
        #     #            lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), game_cpy, display=game.display)
        #    # pmcts = MCTS(game, pnet, args)
        #    # nmcts = MCTS(game, nnet, args)
        #     print('X', end='', flush=True)
        #     def p1(x):
        #         pmcts = MCTS(game_cpy, pnet, args)
        #         print('\t getting probs', flush=True)
        #         probs = pmcts.getActionProb(x, temp=0)
# 
        #         print('\t returning argmax')
        #         return np.argmax(probs)
        #     def p2(x):
        #         nmcts = MCTS(game_cpy, nnet, args)
        #         print('\t getting probs', flush=True)
        #         
        #         probs = nmcts.getActionProb(x, temp=0)
        #         print('\t returning argmax')
        #         return np.argmax(probs)
        #     arena = Arena(p1, p2, game_cpy, display=game_cpy.display)
        #     #return playGame(p1, p2, game_cpy, game_cpy.display, verbose=True)
        #     return arena.playGame(verbose=True)
# 
# 
        # with Pool() as p:
        #     num_compare = args.arenaCompare
        #     results_arena = p.map(f, [(nnet, pnet) for i in range(num_compare)])
        # for gameResult_arena in results_arena:
        #     if gameResult_arena == 1:
        #         oneWon_arena += 1
        #     elif gameResult_arena == -1:
        #         twoWon_arena += 1
        #     else:
        #         draws_arena += 1
# # 
        # arena.player1, arena.player2 = arena.player2, arena.player1
# 
        # with Pool() as p:
        #     results_arena = p.map(f, range(args.arenaCompare))
        # for gameResult_arena in results_arena:
        #     if gameResult_arena == -1:
        #         oneWon_arena += 1
        #     elif gameResult_arena == 1:
        #         twoWon_arena += 1
        #     else:
        #         draws_arena += 1
# 
        # pwins, nwins, draws =  oneWon_arena, twoWon_arena, draws_arena
        # 
        # 
        # 
        # # pwins, nwins, draws = arena.playGamesMultiProcess(args.arenaCompare)
# 
        # 
        # 
        # log.info('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
        # if pwins + nwins == 0 or float(nwins) / (pwins + nwins) < args.updateThreshold:
        #     log.info('REJECTING NEW MODEL')
        #     nnet.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
        # else:
        #     log.info('ACCEPTING NEW MODEL')
        #     nnet.save_checkpoint(folder=args.checkpoint, filename=nnet.getCheckpointFile(i))
        #     nnet.save_checkpoint(folder=args.checkpoint, filename='best.pth.tar')
# 


   # log.info('Loading the Coach...')
  #  c = Coach(g, nnet, args)

   # if args.load_model:
   #     log.info("Loading 'trainExamples' from file...")
   #     c.loadTrainExamples()
#
   # log.info('Starting the learning process 🎉')
   # c.learn()