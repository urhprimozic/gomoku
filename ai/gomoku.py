from logika import Igra, Stanje, Igralec
from vodja import Vodja, VrstaIgralca


def log(self, str, out=None):
    if out is None:
        print(str)
    else:
        with open(out, 'a') as f:
            f.write(str)

class RezultatiIgre():
    '''
    Razred, ki hrani informacije o rezultatu odigrane igre. Začne vedno ČRN (C)
    '''
    def __init__(self, stanje, st_potez):
        '''
        Parametri
        ---------

        stanje (Stanje) - stanje igre na koncu
        st_potez - št potez v igri
        '''
        
        self.stanje = stanje
        self.zmaga_C = (stanje == Stanje.ZMAGA_C)
        self.zmaga_B = (stanje == Stanje.ZMAGA_B)
        self.dolzina_igre = st_potez
    def __str__(self) -> str:
        return f"Stanje igre: {self.stanje}. Dolžina: {self.dolzina_igre}"
    def __iter__(self):
        yield 'stanje', self.stanje
        yield 'zmaga_C', self.zmaga_C
        yield 'zmaga_B', self.zmaga_B 
        yield 'dolzina', self.dolzina_igre
    def tuple(self):
        return (self.stanje, self.dolzina_igre)
        


class Gomoku():

    def odigraj_igro(self, vrsta_igralca_C=VrstaIgralca.C, vrsta_igralca_B=VrstaIgralca.R, logging=2, out=None):
        '''
        Odigra igro med vrsto igralca 1 in 2.
        TODO : verjetno je smiselno nardit objekt "možgani" namesto vrste igralca

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
        vodja.vrsta_igralca[Igralec.C] = vrsta_igralca_C
        vodja.vrsta_igralca[Igralec.B] = vrsta_igralca_B

        vodja.igramo_novo_igro(logging=logging, out=out)
        while vodja.igramo() != 0:
            print("igramo")
        return RezultatiIgre(vodja.koncno_stanje, len(vodja.igra.odigranePoteze))


gomoku = Gomoku()
print(gomoku.odigraj_igro())
