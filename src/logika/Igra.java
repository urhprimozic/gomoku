package logika;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import splosno.Koordinati;

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

    /**
     * Nova igra, v začetni poziciji je prazna in na potezi je O.
     */
    public Igra() {
    	this(15,15);
    }
    
    public Igra(Igra osnovnica){
        this.sirina = osnovnica.sirina;
        this.visina = osnovnica.visina;
        this.plosca = new Polje[visina][sirina];
        for(int v = 0; v < visina; v++){
            for(int s = 0; s < sirina; s++){
                this.plosca[v][s] = osnovnica.plosca[v][s];
            }
        }
        this.naPotezi = osnovnica.naPotezi;
        odigranePoteze = new LinkedList<Poteza>();
        for (Poteza p: osnovnica.odigranePoteze) {
        	odigranePoteze.add(p);
        }
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
        while (x < visina && y < sirina && 0 <= x && 0 <= y) {
            if (plosca[x][y] == igralec.getPolje()) {
                stevec++;
            }
            else {
                //na tem kvadratu ni več pravega žetona
                // če jih je blo prej 5, je zmagal
                if(stevec >= 5){
                    return true;
                }
            	stevec = 0;
            }
            // če je tčn o 5 žetonov, je to točka
            // če jih je paveč kot 5 , pa ne
            
            //if (stevec == 5) {
            //	return true;
            //}
  
            // premik naprej
            x += smer.x;
            y += smer.y;
        }
        return (stevec >= 5);
    }

    public Stanje izracunajNovoStanje() {
    	if (odigranePoteze == null || odigranePoteze.size() == 0) return Stanje.V_TEKU;
    	
        Igralec c = odigranePoteze.getLast().getIgralec();
        Koordinati p = odigranePoteze.getLast().getKoordinati();
        
        int x = p.getX();
        int y = p.getY();
        
        if (petVVrsto(Smer.DOL, c, new Koordinati(Math.max(x-5,0),y))) {
        	return c.zmaga();      
        }
        if (petVVrsto(Smer.DESNO, c, new Koordinati(x, Math.max(0,y-5)))) {
        	return c.zmaga();
        }
        
        int m = Math.min(5, Math.min(x, y));
        if (petVVrsto(Smer.DESNO_DOL, c, new Koordinati(x-m,y-m))) {
        	return c.zmaga();      
        }
        
        int M = Math.min(5, Math.min(visina - x, y));
        if (petVVrsto(Smer.DESNO_DOL, c, new Koordinati(x-M,y-M))) {
        	return c.zmaga();      
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
            Poteza zadnja = odigranePoteze.getLast();
            Koordinati p = zadnja.getKoordinati();
            Igralec c = zadnja.getIgralec();
            
            plosca[p.getX()][p.getY()] = Polje.PRAZNO;
            naPotezi = c;
        }
    }
}