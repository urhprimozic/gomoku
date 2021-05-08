package vodja;

import java.util.Map;

import javax.swing.SwingWorker;

import gui.GlavnoOkno;
import splosno.Koordinati;
import montecarlo.Board;
import montecarlo.Game;
import montecarlo.MonteCarloTreeSearch;
import montecarlo.NNet;

public class Vodja {
	public static final int N = 15;
	
	public static Map<Integer,VrstaIgralca> vrstaIgralca;
	
	public static GlavnoOkno okno;
	
	public static Game igra;
	public static NNet nnet;
	
	public static boolean clovekNaVrsti = false;
	public static MonteCarloTreeSearch mcts;
	
	public static Board plosca;
	public static int igralec;
	
	public static int numPoteze;
		
	public static void igramoNovoIgro () {
		igra = new Game(N);
		nnet = new NNet();
		mcts = new MonteCarloTreeSearch(igra, nnet);
		plosca = new Board(N);
		igralec = 1;
		igramo();
	}
	
	public static void igramo () {
		okno.osveziGUI();
		double stanje = igra.getGameEnded(plosca, igralec);
		
		if (stanje != 0) {
			return; // odhajamo iz metode igramo
		}

		VrstaIgralca vrstaNaPotezi = vrstaIgralca.get(igralec);
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
		Game zacetkaIgra = igra;
		SwingWorker<Koordinati, Void> worker = new SwingWorker<Koordinati, Void> () {
			@Override
			protected Koordinati doInBackground() {
				double[] probs = mcts.getActionProb(plosca);
				double sum = 0;
				double cuttoff = Math.random();
				for (int i = 0; i < probs.length; ++i) {
					if (sum + probs[i] >= cuttoff) {
						return new Koordinati(i / N, i % N);
					}
					sum += probs[i];	
				}
				return null;
			}
			@Override
			protected void done () {
				Koordinati poteza = null;
				try {poteza = get();} catch (Exception e) {e.printStackTrace();};
				if (igra == zacetkaIgra) {
					plosca.executeMove(poteza, igralec);
					igralec *= -1;
					igramo();
				}
			}
		};
		worker.execute();
	}
		
	public static void igrajClovekovoPotezo(Koordinati poteza) {
		plosca.executeMove(poteza, igralec);
		clovekNaVrsti = false;
		igralec *= -1; 
		igramo();
	}


}
