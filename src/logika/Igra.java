package logika;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Deque;

public class Igra {

    // Dimenzije polja
    public int sirina, visina;

    // Igralno polje
    public Polje[][] plosca;

    // Igralec, ki je trenutno na potezi.
    // Vrednost je poljubna, če je igre konec (se pravi, lahko je napačna).
    public Igralec naPotezi;

    // odigrane poteze
    public Deque<Poteza> odigranePoteze;
    
    // stanje igre
    public Stanje trenutnoStanje;

    /**
     * Nova igra, v začetni poziciji je prazna in na potezi je O.
     */
    public Igra() {
    	this(15, 15);
    }
    
    public Igra(int visina, int sirina) {
        plosca = new Polje[visina][sirina];
        for (int i = 0; i < visina; i++) {
            for (int j = 0; j < sirina; j++) {
                plosca[i][j] = Polje.PRAZNO;
            }
        }

        naPotezi = Igralec.C;
        this.sirina = sirina;
        this.visina = visina;
        trenutnoStanje = Stanje.V_TEKU;
        odigranePoteze = new LinkedList<Poteza>();
    }
    
    @Override
    public String toString() {
        String ans = "\nIgra " + Integer.toString(visina) + "x" + Integer.toString(sirina) + "\n";
        for(Polje[] vrstica : plosca){
            for(Polje p : vrstica){
                if (p == Polje.B)ans+=" B ";
                if (p == Polje.C)ans+=" C ";
                if (p == Polje.PRAZNO)ans+=" . ";
            }

            ans += "\n";
        }
    	return ans;
    }

    /**
     * @return seznam vseh možnih potez v tem tenutku poteza je tipa koordinata
     */
    public List<splosno.Koordinati> moznePoteze() {
        // urh
        // Vrne seznam vseh možnih potez v tem tenutku
        // poteza je tipa koordinata
        List<splosno.Koordinati> poteze = new ArrayList<splosno.Koordinati>();
        for (int i = 0; i < visina; i++)
            for (int j = 0; j < sirina; j++)
                if (plosca[i][j] == Polje.PRAZNO)
                    poteze.add(new splosno.Koordinati(i, j));
        return poteze;
    }

    boolean petVVrsto(Smer smer, Igralec igralec, splosno.Koordinati zacetek) {
        // urh
        // True, če je v dani smeri z zacetokv zacetek igralec dosegel točno 5
        // zaporednih
        int x = zacetek.getX();
        int y = zacetek.getY();
        int stevec = 0; // število zaporednih žetonov igralca
        while (x < sirina && y < visina && 0 <= x && 0 <= y) {
            if (plosca[y][x] == igralec.getPolje()) {
                stevec++;
            }
            else {
            	stevec = 0;
            }
            if (stevec >= 5) {
            	return true;
            }
            // premik naprej
            x += smer.x;
            y += smer.y;
        }
        return (stevec >= 5);
    }

    private Stanje izracunajNovoStanje() {
        /* Vrne stanje igre */

        // Najprej preveri, če je trenutni igralec zmagal
        // TODO optimizacija: potrebuje preverit samo presečišča z zadnjo potezo

        // vsi stolpci
        for (int x = 0; x < sirina; x++) {
            if (petVVrsto(Smer.DOL, naPotezi, new splosno.Koordinati(x, 0))) {
                return naPotezi.zmaga();
            }
        }
        // vrstice
        for (int y = 0; y < sirina; y++) {
            if (petVVrsto(Smer.DESNO, naPotezi, new splosno.Koordinati(0, y))) {
                return naPotezi.zmaga();
            }
        }
        // diagonale
        for (int y = 0; y < visina; y++) {
            if (petVVrsto(Smer.DESNO_DOL, naPotezi, new splosno.Koordinati(0, y))) {
                return naPotezi.zmaga();
            }
            else if(petVVrsto(Smer.DESNO_GOR, naPotezi, new splosno.Koordinati(0, y))) {
            	return naPotezi.zmaga();
            }
        }

        // od tukaj dlje vemo, da nihče ni zmagal
        for (Polje[] vrstica : plosca) {
            for (Polje polje : vrstica) {
                if (polje == Polje.PRAZNO) {
                    return Stanje.V_TEKU;
                }
            }
        }
        return Stanje.NEODLOCENO;
    }

    public boolean odigraj(splosno.Koordinati p) {
        int x = p.getX();
        int y = p.getY();
        if (plosca[x][y] == Polje.PRAZNO) {
            plosca[x][y] = naPotezi.getPolje();
            odigranePoteze.add(new Poteza(x, y, naPotezi));
            
            trenutnoStanje = izracunajNovoStanje();

            naPotezi = naPotezi.nasprotnik();
            return true;
        } else {
            return false;
        }
    }

    public void odigrajNakljucnoPotezo() {
        List<splosno.Koordinati> mozne = moznePoteze();
        splosno.Koordinati poteza = mozne.get((int) (Math.random() * mozne.size()));
        if (!odigraj(poteza)) {
            System.out.println(
                    "ERROR - odigrajNakljucno je odigral ilegalno potezo.\n Napaka v moznePoteze()\n ali odigraj()");
        }
    }

    public void razveljaviZadnjo() {
        if (odigranePoteze != null) {
            odigranePoteze.removeLast();
        }
    }
}