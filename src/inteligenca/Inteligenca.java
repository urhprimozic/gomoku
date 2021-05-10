package inteligenca;

import java.util.List;

import logika.Igra;
import splosno.KdoIgra;
import splosno.Koordinati;

public class Inteligenca extends KdoIgra {
	
	private MonteCarloTreeSearch mcts;
	
	public Inteligenca() {
		super("JonMikos + UrhPrimozic");
		mcts = null;
	}
	
	public Koordinati izberiPotezo(Igra igra) {
		if (mcts == null) {
			mcts = new MonteCarloTreeSearch(new NNet(), igra.igralec);
		}
		double[] probs = mcts.getActionProb(igra.board);
		
		double sum = 0;
		double cuttoff = Math.random();
		for (int i = 0; i < probs.length; ++i) {
			if (sum + probs[i] >= cuttoff) {
				return new Koordinati(i / igra.N, i % igra.N);
			}
			sum += probs[i];	
		}
		
		// Fallback plan, should never ever happen but floats are scary
		List<Koordinati> mozne = igra.board.getLegalMoves();
		return mozne.get((int)(Math.random() * mozne.size()));
	}
}
