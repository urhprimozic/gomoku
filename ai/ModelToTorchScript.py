import torch
import torchvision
import numpy as np
import random

from gomoku import GomokuGame
from gomokuNNet import GomokuNNet, NNetWrapper

game = GomokuGame(15)
nnet = NNetWrapper(game)
nnet.load_checkpoint('..', 'best.pth.tar')

nnet.nnet.eval()

board = np.array([[random.randint(-1, 1) for _ in range(15)] for _ in range(15)])
example = torch.FloatTensor(board.astype(np.float64))

traced_module = torch.jit.trace(nnet.nnet, example)
traced_module.save("../GomokuNNet.pt")

