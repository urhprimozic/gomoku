package vodja;

import java.util.List;
import java.util.Map;

import javax.swing.SwingWorker;

import gui.GlavnoOkno;
import inteligenca.MonteCarloTreeSearch;
import inteligenca.NNet;
import logika.Board;
import logika.Game;
import splosno.Koordinati;

public class Vodja {
	public static final int N = 15;
	
	public static Map<Integer,VrstaIgralca> vrstaIgralca;
	
	public static GlavnoOkno okno;
	
	public static Game igra;
	public static NNet nnet;
	
	public static boolean clovekNaVrsti = false;
	public static MonteCarloTreeSearch mcts1;
	public static MonteCarloTreeSearch mcts2;
	
	public static Board plosca;
	public static int igralec;
	
	public static int numPoteze;
		
	public static void igramoNovoIgro () {
		igra = new Game(N);
		nnet = new NNet();
		
		if (vrstaIgralca.get(1) == VrstaIgralca.R) {
			mcts1 = new MonteCarloTreeSearch(igra, nnet, 1);
		
			if (vrstaIgralca.get(-1) == VrstaIgralca.R) {
				mcts2 = new MonteCarloTreeSearch(igra, nnet, -1);
			}
			else {
				mcts2 = null;
			}
		}
		else {
			mcts1 = null;
			if (vrstaIgralca.get(-1) == VrstaIgralca.R) {
				mcts2 = new MonteCarloTreeSearch(igra, nnet, -1);
			}
			else {
				mcts2 = null;
			}
		}
		
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
				double[] probs = null;
				if (igralec == 1) {
					probs = mcts1.getActionProb(plosca);
				}
				if (igralec == -1) {
					probs = mcts2.getActionProb(plosca);
				}
				
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
					if (poteza != null) {
						plosca.executeMove(poteza, igralec);
					}
					else {
						System.out.println("Igramo nakljucno potezo!!! Nekaj je narobe.");
						List<Koordinati> mozne = plosca.getLegalMoves();
						plosca.executeMove(mozne.get((int)(Math.random() * mozne.size())), igralec);
					}
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
