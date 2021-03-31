//package logika;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class Igra {

    public int visina;
    public int sirina;

    // Igralno polje
    private Polje[][] plosca;

    // Igralec, ki je trenutno na potezi.
    // Vrednost je poljubna, če je igre konec (se pravi, lahko je napačna).
    public Igralec naPotezi;

    /**
     * Nova igra, v začetni poziciji je prazna in na potezi je O.
     */
    public Igra(int visina, int sirina) {
        // Jon
        plosca = new Polje[N][N];
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                plosca[i][j] = Polje.PRAZNO;
            }
        }
        naPotezi = Igralec.O;
    }

    /**
     * @return seznam možnih potez
     */
    public List<Koordinati> moznePoteze() {
        // urh
        // Vrne seznam vseh možnih potez v tem tenutku
        // poteza je tipa koordinata
        List<Koordinati> poteze = new ArrayList<Koordinati>();
        for (int i = 0; i < visina; i++)
            for (int j = 0; j < sirina; j++)
                if (plosca[i][j] == Polje.PRAZNO)
                    poteze.add(new Koordinati(i, j));
        return poteze;
    }

    boolean petVVrsto(Smer smer, Igralec igralec, Koordinati zacetek) {
        // urh
        // True, če je v dani smeri z zacetokv zacetek igralec dosegel točno 5
        // zaporednih
        int x = zacetek.getX();
        int y = zacetek.getY();
        int stevec = 0; // število zaporednih žetonov igralca
        while (x < sirina && y < visina) {
            if (plosca[x][y] == igralec.getPolje())
                stevec++;
            // tok se je prekinil
            else {
                if (stevec == 5)
                    return true;
                stevec = 0;
            }
            // premik naprej
            x += smer.x;
            y += smer.y;
        }
        return false;
    }

    public Stanje stanje() {
        /* Vrne stanje igre */

        // Najprej preveri, če je trenutni igralec zmagal
        // TODO optimizacija: potrebuje preverit samo presečišča z zadnjo potezo

        // vsi stolpci
        for (int x = 0; x < sirina; x++)
            if (petVVrsto(Smer.dol(), naPotezi, new Koordinati(x, 0)))
                return naPotezi.zmaga();
        // vrstice
        for (int y = 0; y < sirina; y++)
            if (petVVrsto(Smer.desno(), naPotezi, new Koordinati(0, y)))
                return naPotezi.zmaga();
        // diagonale
        for (int y = 0; y < visina; y++)
            if (petVVrsto(Smer.desnoDol(), naPotezi, new Koordinati(0, y)))
                return naPotezi.zmaga();

        // od tukaj dlje vemo, da nihče ni zmagal
        for (Polje[] vrstica : plosca)
            for (Polje polje : vrstica)
                if (polje == Polje.PRAZNO)
                    return Stanje.V_TEKU;
        return Stanje.NEODLOCENO;
    }

    public boolean odigraj(Koordinati p) {
        // jon
        // true - če je bla uspešno odigrana poteza

        if (plosca[p.getX()][p.getY()] == Polje.PRAZNO) {
            plosca[p.getX()][p.getY()] = naPotezi.getPolje();
            naPotezi = naPotezi.nasprotnik();
            return true;
        } else {
            return false;
        }
    }

    public void razveljaviZadnjo() {
        // jon
        // dodaj nek seznam odigranih
    }
}