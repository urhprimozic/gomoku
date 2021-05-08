from logika import Igra, Stanje, Igralec
from vodja import Vodja, VrstaIgralca


def log(self, str, out=None):
    if out is None:
        print(str)
    else:
        with open(out, 'a') as f:
            f.write(str)
#slaba slbala lasdabasdgv
#class RezultatiIgre():
#    '''
#    Razred, ki hrani informacije o rezultatu odigrane igre. Začne vedno ČRN (C)
#    '''
#    def __init__(self, stanje, st_potez):
#        '''
#        Parametri
#        ---------
#
#        stanje (Stanje) - stanje igre na koncu
#        st_potez - št potez v igri
#        '''
#        
#        self.stanje = stanje
#        self.zmaga_C = (stanje == Stanje.ZMAGA_C)
#        self.zmaga_B = (stanje == Stanje.ZMAGA_B)
#        self.dolzina_igre = st_potez
#    def __str__(self) -> str:
#        return f"Stanje igre: {self.stanje}. Dolžina: {self.dolzina_igre}"
#    def __iter__(self):
#        yield 'stanje', self.stanje
#        yield 'zmaga_C', self.zmaga_C
#        yield 'zmaga_B', self.zmaga_B 
#        yield 'dolzina', self.dolzina_igre
#    def tuple(self):
#        return (self.stanje, self.dolzina_igre)
        


class Gomoku():

    def odigraj_igro(self, igralec1=None, igralec2=None, logging=2, out=None):
        '''
        Odigra igro med vrsto igralca 1 in 2.
        TODO : verjetno je smiselno nardit objekt "možgani" namesto vrste igralca

        Parametri
        ---------
            igralec1, igralec2 (function) - funckija , ki sprejme stanje polja {-1,0,1}^225 in vrne action
        
        
        logging - integer (TODO a spremenimo?)

            0 - brez loginga
            1 - le zmage
            2 - igralna plošča vsak korak


        out (str) - 
            filename od datoteke za logging 
            (None za standardni output)
        
        Returns
        --------
        stanje igre na koncu (stanje.Stanje())
        '''
        vodja = Vodja(igralec1, igralec2)

        vodja.igramo_novo_igro(logging=logging, out=out)
        while True:
            stanje = vodja.igramo()
            if stanje is None:
                continue
            return stanje 
        


# gomoku = Gomoku()
# print(gomoku.odigraj_igro())
