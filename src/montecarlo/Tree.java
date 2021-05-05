package montecarlo;

import logika.Igra;

public class Tree {
	public Node root;
	
	public Tree() {
		root = new Node(new State(new Igra()));
	}
}
