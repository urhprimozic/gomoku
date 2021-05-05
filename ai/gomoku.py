from logika import Igra, Stanje
from vodja import Vodja


class Gomoku():
    def log(self, str, out=None):
        if out is None:
            print(str)
        else:
            with open(out, 'a') as f:
                f.write(str)

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
        vodja = Vodja()
        vodja.igramo_novo_igro(logging=logging, out=out)
        while vodja.igramo() != 0:
            self.log("Igramo")

g = Gomoku()
g.igraj()