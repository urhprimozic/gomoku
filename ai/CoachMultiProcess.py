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

args = dotdict({
    'numIters': 10,
    'numEps': 50,#100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 90000, #200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 12, #25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40, #40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 3,

    'checkpoint': './test_2/',
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
        log.info('Running Episode!')
        trainExamples = []
        board = game.getInitBoard()
        curPlayer = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard = game.getCanonicalForm(board, curPlayer)
            temp = int(episodeStep < args.tempThreshold)

            pi = mcts.getActionProb(canonicalBoard, temp=temp)
            sym = game.getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, curPlayer, p, None])

            action = np.random.choice(len(pi), p=pi)
            board, curPlayer = game.getNextState(board, curPlayer, action)

            r = game.getGameEnded(board, curPlayer)

            if r != 0:
                return [(x[0], x[2], r * ((-1) ** (x[1] != curPlayer))) for x in trainExamples]

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
                try:
                   # Multithreading: 
                   # with dummy.Pool() as p:
                    with Pool(NUMBER_OF_CORES) as p:
                        # logging.info('we in pool bojs')
                        raw = p.map(executeEpisode,range(args.numEps))
                    iterationTrainExamples = deque(raw)
                    logging.info('pool finished')
                except Exception:
                    logging.exception('sth wrong', stacklevel=20, stack_info=True)
                    exit()
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



   # log.info('Loading the Coach...')
  #  c = Coach(g, nnet, args)

   # if args.load_model:
   #     log.info("Loading 'trainExamples' from file...")
   #     c.loadTrainExamples()
#
   # log.info('Starting the learning process 🎉')
   # c.learn()