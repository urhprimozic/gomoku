import sys
import enum
from logika import Igra, Stanje


class VrstaIgralca(enum.Enum):
    R = 0
    C = 1

    def __str__(self):
        if self == VrstaIgralca.R:
            return 'računalnik'
        return 'človek'


class Gomoku():
    def log(str, out=None):
        if out is None:
            print(str)
        else:
            with open(out, 'a') as f:
                f.write(str)

    def igraj(logging=2, out=None):
        '''
        Odigra igro.

        Parametri
        ---------
        logging - integer

            0 - brez loginga
            1 - le zmage
            2 - igralna plošča vsak korak
        

        out (str) - 
            filename od datoteke za logging 
            (None za standardni output)
        '''
        while true:
            igra = Igra()
