import logging
from multiprocessing import Pool, dummy
from platform import win32_edition
import coloredlogs
from Arena import Arena
from gomoku import GomokuGame
import numpy as np
import threading

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


if __name__ == "__main__":
    log.info('Normal:')
    N = 50000
    ans = []
    for i in range(1,N):
        ans.append(f(i))
    log.info('finished')
   # print(ans[:10])
    
    ans = []
    log.info('pool:')
    with Pool() as p:
        ans = p.map(f, range(1,N))
    log.info('finished')
   # print(ans[:10])

    ans = []
    log.info('pool-threading:')
    with dummy.Pool() as p:
        ans = p.map(f, range(1,N))
    log.info('finished')
   # print(ans[:10])

