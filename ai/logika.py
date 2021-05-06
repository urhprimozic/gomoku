import enum
import random


class Polje(enum.Enum):
    C = 0
    B = 1
    PRAZNO = 2


class Stanje(enum.Enum):
    V_TEKU = 0
    ZMAGA_C = 1
    ZMAGA_B = 2
    NEODLOCENO = 3


class Igralec(enum.Enum):
    C = 0
    B = 1

    def nasprotnik(self):
        if self == Igralec.C:
            return Igralec.B
        return Igralec.C

    def get_polje(self):
        if self == Igralec.C:
            return Polje.C
        return Polje.B

    def zmaga(self):
        if self == Igralec.C:
            return Stanje.ZMAGA_C
        return Stanje.ZMAGA_B

# namesto poteze in smeri imam tuple (tko delamo proji)


class Igra():
    def __init__(self, sirina=15, visina=15):
        self.sirina = sirina
        self.visina = visina
        self.plosca = [[Polje.PRAZNO for i in range(
            sirina)] for i in range(visina)]
        self.naPotezi = Igralec.C
        self.trenutnoStanje = Stanje.V_TEKU
        # linked list ---> List
        self.odigranePoteze = []

    def __str__(self):
        ans = f"\nIgra {self.visina}x{self.sirina}\n"
        for vrstica in self.plosca:
            for p in vrstica:
                if p == Polje.B:
                    ans += " B "
                elif p == Polje.C:
                    ans += " C "
                elif p == Polje.PRAZNO:
                    ans += " . "
                else:
                    raise TypeError(
                        f"Buraz, polje[*][*] = {str(p)} je tipa {str(type(p))}, mogu bi pa bit Polje")
            ans += "\n"
        return ans

    def mozne_poteze(self):
        '''Vrne seznam vseh možnih potez (tuplov)'''
        poteze = []
        for i in range(self.visina):
            for j in range(self.sirina):
                if self.plosca[i][j] == Polje.PRAZNO:
                    poteze.append((i, j))
        return poteze
    # Dogovor: (vrstica, stolpec)

    def pet_v_vrsto(self, smer, igralec, zacetek):
        '''True, če je v dani smeri z zacetkom v 
         zacetek igralec dosegu tocno pet zaporednih '''
        vrstica = zacetek[0]
        stolpec = zacetek[1]
        stevec = 0  # število zaporednih žetonov igralca

        while vrstica >= 0 and vrstica < self.visina and stolpec >= 0 and stolpec < self.sirina:
            if self.plosca[vrstica][stolpec] == igralec.get_polje():
                stevec += 1
            else:
                if stevec == 5:
                    return True
                stevec = 0
            vrstica += smer[0]
            stolpec += smer[1]
        return stevec == 5

    def izracunaj_novo_stanje(self):
        '''Vrne stanje igre '''
        # TODO optimizacija (preveri le presečišče z zadnjo potezo)

        #(vrstca, stolpec)
        DOL = (1, 0)
        DESNO = (0, 1)
        DESNO_DOL = (1, 1)
        DESNO_GOR = (-1, 1)

        # stolpci
        for stolpec in range(self.sirina):
            if self.pet_v_vrsto(DOL, self.naPotezi, (0, stolpec)):
                return self.naPotezi.zmaga()

        # vrstice
        for vrstica in range(self.visina):
            if self.pet_v_vrsto(DESNO, self.naPotezi, (vrstica, 0)):
                return self.naPotezi.zmaga()

        # diagonale pod glavno diagonalo
        for vrstica in range(self.visina):
            if self.pet_v_vrsto(DESNO_DOL, self.naPotezi, (vrstica, 0)):
                return self.naPotezi.zmaga()
            if self.pet_v_vrsto(DESNO_GOR, self.naPotezi, (vrstica, 0)):
                return self.naPotezi.zmaga()

        # diagonale nad glavno diagonalo
        for stolpec in range(1, self.sirina):
            if self.pet_v_vrsto(DESNO_DOL, self.naPotezi, (0, stolpec)):
                return self.naPotezi.zmaga()
            if self.pet_v_vrsto(DESNO_GOR, self.naPotezi, (0, stolpec)):
                return self.naPotezi.zmaga()

        # če smo tukaj, nihče ni zmagal
        if len(self.mozne_poteze()) == 0:
            # če ni več možnih potez, smo konc
            return Stanje.NEODLOCENO

        return Stanje.V_TEKU

    def odigraj(self, p):
        vrstica = p[0]
        stolpec = p[1]

        if self.plosca[vrstica][stolpec] == Polje.PRAZNO:
            self.plosca[vrstica][stolpec] = self.naPotezi.get_polje()
            self.odigranePoteze.append((vrstica, stolpec, self.naPotezi))
            
            self.trenutnoStanje = self.izracunaj_novo_stanje()
            self.naPotezi = self.naPotezi.nasprotnik()
            return True
        # če ne ni šlo
        #raise Warning("Napačna poteza! Polje je že zasedeno")
        print("WARNING!\n\tNapačna poteza! Polje je že zasedeno")
        return False

    def odigraf_nakljucno_potezo(self):
        mozne = self.mozne_poteze()
        if len(mozne) == 0:
            print("WARNING: ni mogoče odigrati naključne poteze, ker ni možnih potez!")
        poteza = random.choice(mozne)
        if not self.odigraj(poteza):
            print(
                "ERROR - odigrajNakljucno je odigral ilegalno potezo.\n Napaka v moznePoteze()\n ali odigraj()")

    # TODO a rabmo še razveljavi zadnjo??