from collections import deque
from random import shuffle
from args import args
from gomoku import GomokuGame
from gomokuNNet import NNetWrapper as nn
from Arena import Arena
import logging
from MCTS import MCTS
import sys
import pickle
import argparse
import numpy as np

# log = logging.getLogger(__name__)


def getCheckpointFile(iteration):
    return 'checkpoint_' + str(iteration) + '.pth.tar'

if __name__ == "__main__":
    # parse data
    parser = argparse.ArgumentParser()
   # parser.add_argument("-f", "--folder", default="./default_trained/")
    parser.add_argument("-i", "--iteration", default="0")
    parsed_args = sys.argv[1:]
    parsed = parser.parse_args(parsed_args)
    iteration = parsed.iteration
    #folder_name = parsed.folder

    with open(f'data/results_{iteration}.txt', 'rb') as f:
        raw = pickle.load(f)
    with open(f'data/trainExamplesHistory.txt', 'rb') as f:
        trainExamplesHistory = pickle.load(f)

    iterationTrainExamples = deque(raw)
    # save the iteration examples to the history
    trainExamplesHistory.append(iterationTrainExamples)
    if len(trainExamplesHistory) > args.numItersForTrainExamplesHistory:
        logging.warning(
            f"Removing the oldest entry in trainExamples. len(trainExamplesHistory) = {len(trainExamplesHistory)}")
        trainExamplesHistory.pop(0)

    trainExamples = []
    for e in trainExamplesHistory:
        trainExamples.extend(e)

    # getting new nets
    game = GomokuGame(15)
    nnet = nn(game)
    pnet = nnet.__class__(game)

    # learning
    nnet.load_checkpoint(folder=args.checkpoint, filename='lastNet.pth.tar')
    # training new network, keeping a copy of the old one
    nnet.save_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
    pnet.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
    pmcts = MCTS(game, pnet, args)

    nnet.train(trainExamples)
    nmcts = MCTS(game, nnet, args)

    logging.info('PITTING AGAINST PREVIOUS VERSION')
    arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                  lambda x: np.argmax(nmcts.getActionProb(x, temp=0)), game)
    pwins, nwins, draws = arena.playGames(args.arenaCompare)

    logging.info('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
    if pwins + nwins == 0 or float(nwins) / (pwins + nwins) < args.updateThreshold:
        logging.info('REJECTING NEW MODEL')
        nnet.load_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')
    else:
        logging.info('ACCEPTING NEW MODEL')
        nnet.save_checkpoint(folder=args.checkpoint,
                             filename=getCheckpointFile(iteration))
        nnet.save_checkpoint(folder=args.checkpoint, filename='best.pth.tar')
    # lastNet je zmeri mreža
    nnet.load_checkpoint(folder=args.checkpoint, filename='lastNet.pth.tar')
    shuffle(trainExamples)
