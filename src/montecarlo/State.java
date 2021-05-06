package montecarlo;

import java.util.LinkedList;
import java.util.List;

import logika.Igra;
import splosno.Koordinati;

public class State {
	public Igra board;
	public int visitCount;
	public double winScore;
	
	public State(State s) {
		board = new Igra(s.board);
		visitCount = s.visitCount;
		winScore = s.winScore;
	}
	
	public State(Igra b) {
		board = b;
		visitCount = 0;
		winScore = 0;
	}
	
	public List<State> getAllPossibleStates() {
		List<State> states = new LinkedList<State>();
		for (Koordinati p : board.moznePoteze()) {
			Igra b = new Igra(board);
			b.odigraj(p);
			states.add(new State(b));
		}
		return states;
	}
	
	public void randomPlay(List<Koordinati> moves) {
		int index = ((int) (Math.random() * moves.size()));
		Koordinati p = moves.get(index);
		board.odigraj(p);
		moves.remove(index);
	}
}
