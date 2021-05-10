# DEPRECATED!!


# povzeto po https://github.com/suragnair/alpha-zero-general/blob/master/Coach.py
import logging
import os
import sys
from collections import deque
from pickle import Pickler, Unpickler
from random import shuffle
import numpy as np
from tqdm import tqdm
#from arena import Arena
from MCTS import MCTS
import threading
import logika

log = logging.getLogger(__name__)

class Trening():
    '''
    Self play + learning. maanjše razlike z virom
    '''
    def __init__(self, nnet, st_iger=200) -> None:
        '''
        nnet - nevronska mreža. Ne dela z drugimi policyji

        st_iger - st iger igranih v eni epizodi
        (se mi zdi smiselno nastavnt na 200, sj mamo multithreading)
        '''
        self.nnet = nnet
        self.trainExamplesHistory = []
        self.preskociPrvoIgro = False

        def executeEpisode(self):
            """
            This function executes one episode of self-play, starting with player 1.
            As the game is played, each turn is added as a training example to
            trainExamples. The game is played till the game ends. After the game
            ends, the outcome of the game is used to assign values to each example
            in trainExamples.
            It uses a temp=1 if episodeStep < tempThreshold, and thereafter
            uses temp=0.
            Returns:
                trainExamples: a list of examples of the form (canonicalBoard, currPlayer, pi,v)
                            pi is the MCTS informed policy vector, v is +1 if
                            the player eventually won the game, else -1.
            """
            trainExamples = []
            board = self.game.getInitBoard()
            self.curPlayer = 1
            episodeStep = 0

            while True:
                episodeStep += 1
                canonicalBoard = self.game.getCanonicalForm(board, self.curPlayer)
                temp = int(episodeStep < self.args.tempThreshold)

                pi = self.mcts.getActionProb(canonicalBoard, temp=temp)
                sym = self.game.getSymmetries(canonicalBoard, pi)
                for b, p in sym:
                    trainExamples.append([b, self.curPlayer, p, None])

                action = np.random.choice(len(pi), p=pi)
                board, self.curPlayer = self.game.getNextState(board, self.curPlayer, action)

                r = self.game.getGameEnded(board, self.curPlayer)

                if r != 0:
                    return [(x[0], x[2], r * ((-1) ** (x[1] != self.curPlayer))) for x in trainExamples]
