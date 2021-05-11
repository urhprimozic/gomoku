import logging
import coloredlogs
from Arena import Arena
from gomoku import GomokuGame
import numpy as np

log = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

actions_raw =[(i, j) for i in range(15)
                    for j in range(15)]


def human_player(_):
    v = int(input("Vrstica: "))
    s = int(input("Stolpec: "))
    return actions_raw.index((v, s))


def test_arena(num):
    log.info(f'Testing Arena.playGames({num})')
    game = GomokuGame(15)
    arena = Arena(human_player, human_player, game, game.display)
    arena.playGames(num, True)


if __name__ == "__main__":
    test_arena(4)
