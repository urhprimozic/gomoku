# prepeares map data
import os
from gomoku import GomokuGame
from args import args
from gomokuNNet import NNetWrapper as nn
import pickle

def empty(dir):
    os.makedirs(os.path.dirname(dir), exist_ok=True)
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

#empties /data/
if __name__ == '__main__':
    empty('./data/')
    empty(args.checkpoint)
    

    game = GomokuGame(15)
    nnet = nn(game)
    nnet.save_checkpoint(folder=args.checkpoint, filename='lastNet.pth.tar')
    nnet.save_checkpoint(folder=args.checkpoint, filename='temp.pth.tar')

    with open(f'data/trainExamplesHistory.txt', 'wb') as f:
        trainExamplesHistory = []
        trainExamplesHistory = pickle.dump(trainExamplesHistory, f)

    