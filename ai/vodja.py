# DEPRECATED!!

import enum
from logika import Igra, Igralec, Polje, Stanje


def log(str, out=None):
    if out is None:
        print(str)
    else:
        with open(out, 'a') as f:
            f.write(str)


class VrstaIgralca(enum.Enum):
    R = 0
    C = 1

    def __str__(self):
        if self == VrstaIgralca.R:
            return 'računalnik'
        return 'človek'

def convert(polje):
    if  polje ==Polje.PRAZNO:
        return 0
    if  polje ==Polje.C:
        return 1
    if  polje ==Polje.B:
        return -1
    return 0

class Vodja():
    # statične:
   # igra = None
#     clovek_na_vrsti = False
   # igralec = {}
    def __init__(self, igralec1, igralec2) -> None:
        '''
             igralec1, igralec2 (function) - funckija , ki sprejme stanje polja {-1,0,1}^225 in vrne action
        '''
        self.igra = None
        self.clovek_na_vrsti = False
        self.igralca = {Igralec.C : igralec1, Igralec.B : igralec2}

    def igramo(self, logging=2, out=None):
        self.koncno_stanje = None
        if self.igra is None:
            raise Exception(f"igramo() klicano, vendar {self} nima igre")
        
        if len(self.igra.odigranePoteze) > 0:
            if(logging >= 2):
                log(str(self.igra.odigranePoteze[-1]
                        ) + str(self.igra.trenutnoStanje))
        if logging >= 2:
            log(self.igra.__str__())

        if self.igra.trenutnoStanje == Stanje.ZMAGA_C or self.igra.trenutnoStanje == Stanje.ZMAGA_B or self.igra.trenutnoStanje == Stanje.NEODLOCENO:
            self.koncno_stanje = self.igra.trenutnoStanje
            return self.koncno_stanje
        # drugače je pa še v teku
        igralec = self.igra.naPotezi
        mozgani = self.igralca.get(igralec)
        if mozgani is None:
            self.igrajClovekovoPotezo()
        else:
            # #" self.igrajRacunalnikovoPotezo()
            #mozgani.igrajPotezo(self.igra.plosca)
            raw = list(map(lambda vrstica : list(map(lambda v : convert(v),vrstica)), self.igra.plosca))
            mozgani(raw)
        return None

    def igrajClovekovoPotezo(self):
        vrstica = int(input("Vrstica: "))
        stolpec = int(input("Stolpec: "))
        #dejanska kopija
       # kopija = self.igra
        self.igra.odigraj((vrstica, stolpec))
    
    def igrajRacunalnikovoPotezo(self):
        log("WARNING - igrajRacunalnikovoPotezo se ni pravilno implementirana in igra naključno!")
        self.igra.odigraf_nakljucno_potezo()


    def igramo_novo_igro(self, logging=2, out=None):
        self.igra = Igra()
        self.koncno_stanje = None
        if logging > 0:
            log("New game created")

        self.igramo(logging, out)
