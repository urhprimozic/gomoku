import enum
from logika import Igra, Stanje


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


class Vodja():
    # statične:
    igra = None
    clovek_na_vrsti = False
    vrsta_igralca = {}

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
            return 0
        # drugače je pa še v teku
        igralec = self.igra.naPotezi
        vrstaNaPotezi = self.vrsta_igralca.get(igralec)
        if vrstaNaPotezi is None:
            raise Exception("vrstaNaPotezi is None! Ali si pozabil nastavit Vodja.vrsta_igralca = {...}?")
        if vrstaNaPotezi == VrstaIgralca.C:
            self.igrajClovekovoPotezo()
        else:
            self.igrajRacunalnikovoPotezo()

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
