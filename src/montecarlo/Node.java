package montecarlo;

import java.util.LinkedList;
import java.util.List;

import splosno.Koordinati;

public class Node {
	public State state;
	public Node parent;
	public List<Node> childArray;
	
	public Node(State s) {
		state = s;
		parent = null;
		childArray = new LinkedList<Node>();
	}
	
	public Node(Node n) {
		state = new State(n.state);
		parent = n.parent;
	}
	
	public Node randomChild() {
		return childArray.get((int) (Math.random() * childArray.size()));
	}
	
	public Node bestChild() {
		Node best = childArray.get(0);
		double mostVisits = best.state.visitCount;
		for (Node child : childArray) {
			Koordinati p = child.state.board.odigranePoteze.getLast().getKoordinati();
			if (child.state.visitCount >= mostVisits) {
				best = child;
				mostVisits = child.state.visitCount;
			}
		}
		return best;
	}
}
