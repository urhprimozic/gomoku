from logika import Igra, Stanje
from vodja import Vodja


def log(self, str, out=None):
    if out is None:
        print(str)
    else:
        with open(out, 'a') as f:
            f.write(str)
class Gomoku():

    def igraj(self, logging=2, out=None):
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
        # brez vodje
        self.igra = Igra()

        if logging > 0:
            log("New game created")