//package logika;

import java.util.LinkedList;
import java.util.Deque;

public class Igra {

	// Dimenzije polja
	public int sirina, visina;
	
	// Igralno polje
	private Polje[][] plosca;
	
	// Igralec, ki je trenutno na potezi.
	// Vrednost je poljubna, če je igre konec (se pravi, lahko je napačna).
	public Igralec naPotezi;
	
	// odigrane poteze
	public Deque<Poteza> odigranePoteze;


	/**
	 * Nova igra, v začetni poziciji je prazna in na potezi je O.
	 */
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
	

	/**
	 * @return seznam možnih potez
	 */
	public LinkedList<Koordinati> moznePoteze() {
        //urh
        // More vrnt seznam vseh možnih potez v tem trenutnku
        // poteza je tipa koordinata
		return null;
	}


    boolean petVVrsto(Smer smer, Igralec igralec, Koordinati zacetek){
        //urh
            // True, če je v dani smeri z zacetokv zacetek igralec dosegel točno 5 zaporednih
            return false;
    }
	


	public Stanje stanje() {
        //urh
		// Ali imamo zmagovalca?
		//al je neoodčlocen
		return Stanje.NEODLOCENO;
	}


	public boolean odigraj(Koordinati p) {
		int x = p.getX();
		int y = p.getY();
		if (plosca[x][y] == Polje.PRAZNO) {
			plosca[x][y] = naPotezi.getPolje();
			odigranePoteze.add(new Poteza(x, y, naPotezi));
			
			naPotezi = naPotezi.nasprotnik();
			return true;
		}
		else {
			return false;
		}
	}
    public void razveljaviZadnjo(){
        if (odigranePoteze != null) {
        	odigranePoteze.removeLast();
        }
    }
}