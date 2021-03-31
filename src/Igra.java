//package logika;

import java.util.LinkedList;
import java.util.List;

public class Igra {

	
	// Velikost igralne pološče je N x N.
	public static final int N = 3;

	
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
        //urh
        // More vrnt seznam vseh možnih potez v tem trenutnku
        // poteza je tipa koordinata
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
        //jon
        //true - če je bla uspešno odigrana poteza
    
		if (plosca[p.getX()][p.getY()] == Polje.PRAZNO) {
			plosca[p.getX()][p.getY()] = naPotezi.getPolje();
			naPotezi = naPotezi.nasprotnik();
			return true;
		}
		else {
			return false;
		}
	}
    public void razveljaviZadnjo(){
        //jon
        // dodaj nek seznam odigranih
    }
}