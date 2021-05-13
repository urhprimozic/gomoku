import logging
from multiprocessing import Pool, dummy
from platform import win32_edition
import coloredlogs
from Arena import Arena
from MCTS import MCTS
from gomoku import GomokuGame
import numpy as np
from utils import dotdict
from gomokuNNet import GomokuNNet, NNetWrapper

log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

actions_raw =[(i, j) for i in range(15)
                    for j in range(15)]


def human_player(_):
    v = int(input("Vrstica: "))
    s = int(input("Stolpec: "))
    return actions_raw.index((v, s))


def test_arena_by_hand(num):
    log.info(f'Testing Arena.playGames({num})')
    game = GomokuGame(15)
    arena = Arena(human_player, human_player, game, game.display)
    arena.playGames(num, True)
moves = []

def test_arena(filename='tests.txt'):
    global moves 
    with open(filename, 'r') as f:
        plays = f.read().split('\n\n')
        for play in plays:
            moves = play.split('\n')[::-1] + play.split('\n')[::-1]
            moves = list(map(lambda s : (int(s.split(',')[0]), int(s.split(',')[1])), moves))
            game = GomokuGame(15)
            
            def f(_):
                global moves
                ans = actions_raw.index(moves[-1])
                moves = moves[:-1]
                return ans
            arena = Arena(f, f, game, game.display)
            try:
                arena.playGames(2, True)
            except:
                print('continuing\n')
        
def collatz(n):
    if n % 2 == 0:
        return n/2
    return 3*n + 1
def f(n):
    # print(f'calculating f{n}')
    ans = n
    step = 0
    while ans != 1:
        ans = collatz(ans)
        step += 1
    return step

def nn_move(board, mcts, player, game):
    canonicalBoard = game.getCanonicalForm(board, player)
    pi = mcts.getActionProb(canonicalBoard, temp=0)
    return np.argmax(pi)
    #return  np.random.choice(len(pi), p=pi)

def human_vs_nn(num, nnet,  args, game):
    '''
    num - število iger za arena()
    nnet- nevronska mreža
    '''
    #game = GomokuGame(15)
    mcts = MCTS(game, nnet, args)
    # -1 ker je drugi
    arena = Arena(human_player, lambda b :  np.argmax(mcts.getActionProb(b, temp=0)), game, display=game.display)#nn_move(b, mcts, -1, game)
    arena.playGames(num, verbose=True)

args = dotdict({
    'numIters': 10,
    'numEps': 50,#100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 90000, #200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 500, #25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40, #40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,
    'timeLimit' :4.9, 

    'checkpoint': './test_1/',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})
if __name__ == "__main__":
    game = GomokuGame(15)
    nnet = NNetWrapper(game)
    # nnet.load_checkpoint(folder='tests/test_0_small', filename='temp.pth.tar')#filename='best.pth.tar')
    human_vs_nn(4, nnet, args, game)



