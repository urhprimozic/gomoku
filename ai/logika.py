import enum


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
                if p == Polje.C:
                    ans += " C "
                if p == Polje.PRAZNO:
                    ans += " . "
                else:
                    raise TypeError(
                        f"Buraz, polje[*][*] je tipa {str(type(p))}, mogu bi pa bit Polje")
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
