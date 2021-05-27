package vodja;

import java.util.Map;

import javax.swing.SwingWorker;

import ai.djl.translate.TranslateException;
import gui.GlavnoOkno;
import inteligenca.Inteligenca;
import logika.Game;
import logika.Igra;
import splosno.Koordinati;

public class Vodja {
	public static final int N = 15;
	
	public static Map<Integer,VrstaIgralca> vrstaIgralca;
	
	public static GlavnoOkno okno;
	
	public static Igra igra;
	
	public static boolean clovekNaVrsti = false;
	
	public static Inteligenca comp1;
	public static Inteligenca comp2;
		
	public static void igramoNovoIgro () {
		igra = new Igra();
		
		if (vrstaIgralca.get(1) == VrstaIgralca.R) {
			comp1 = new Inteligenca();
		}
		else {
			comp1 = null;
		}
		
		if (vrstaIgralca.get(-1) == VrstaIgralca.R) {
			comp2 = new Inteligenca();
		}
		else {
			comp2 = null;
		}
		
		igramo();
	}
	
	public static void igramo () {
		okno.osveziGUI();
		double stanje = Game.getGameEnded(igra.board, igra.igralec);
		
		if (stanje != 0) {
			return; // odhajamo iz metode igramo
		}

		VrstaIgralca vrstaNaPotezi = vrstaIgralca.get(igra.igralec);
		switch (vrstaNaPotezi) {
		case C: 
			clovekNaVrsti = true;
			break;
		case R:
			igrajRacunalnikovoPotezo();
			break;
		}
	}

	
	public static void igrajRacunalnikovoPotezo() {
		Igra zacetnaIgra = igra;
		SwingWorker<Koordinati, Void> worker = new SwingWorker<Koordinati, Void> () {
			@Override
			protected Koordinati doInBackground() throws TranslateException {
				if (igra.igralec == 1) {
					return comp1.izberiPotezo(igra);
				}
				else {
					return comp2.izberiPotezo(igra);
				}
			}
			@Override
			protected void done () {
				Koordinati poteza = null;
				try {poteza = get();} catch (Exception e) {e.printStackTrace();};
				if (igra == zacetnaIgra) {
					igra.odigraj(poteza);
					igramo();
				}
			}
		};
		worker.execute();
	}
		
	public static void igrajClovekovoPotezo(Koordinati poteza) {
		igra.odigraj(poteza);
		clovekNaVrsti = false;
		igramo();
	}


}
