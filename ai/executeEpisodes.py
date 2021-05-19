from multiprocessing import Pool
import pickle
from gomokuNNet import NNetWrapper as nn
from gomoku import GomokuGame
from args import args
from MCTS import MCTS
import sys
import argparse
import numpy as np



def executeEpisode(_):


    # PREPERATIONS  
    # game
    game = GomokuGame(15)

    # neural net(load or new, if iter = 0)
    nnet = nn(game)
    if iteration != 0:
        # mamo že staro mrežo iz prejšne iteracije
        nnet.load_checkpoint(folder=args.checkpoint, filename='lastNet.pth.tar')

    #monte carlo tree
    mcts = MCTS(game, nnet, args)
        

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
            # with open(f'data/ep_{iteration}.txt', 'w') as f:
            #     ans = [(x[0], x[2], r * ((-1) ** (x[1] != curPlayer))) for x in trainExamples]
            #     pickle.dump(ans, f)
            #     break
            return [(x[0], x[2], r * ((-1) ** (x[1] != curPlayer))) for x in trainExamples]
    
if __name__ == "__main__":
    # parse data 
    parser = argparse.ArgumentParser()
    #parser.add_argument("-f", "--folder", default="./default_trained/")
    parser.add_argument("-i", "--iteration", default="0")
    parsed_args = sys.argv[1:]
    parsed = parser.parse_args(parsed_args)
    iteration = parsed.iteration
   # folder_name = parsed.folder
    
    with Pool() as p:
        results = p.map(executeEpisode, range(args.numEps))
    
    with open(f'data/results_{iteration}.txt', 'wb') as f:
        pickle.dump(results, f)
