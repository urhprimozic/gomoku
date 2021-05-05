package montecarlo;

import java.util.List;

import logika.Igra;
import logika.Stanje;
import splosno.Koordinati;

public class MonteCarloTreeSearch {
	static final int WIN_SCORE = 1;
	public int level;
	
	public Koordinati findNextMove(Igra board) {		
		long end = System.currentTimeMillis() + 5000;
				
		Tree tree = new Tree();
		Node root = tree.root;
		
		root.state = new State(board);
		
		int i = 0;
		while (System.currentTimeMillis() < end) {
			Node promisingNode = selectPromisingNode(root);
			if (promisingNode.state.board.trenutnoStanje == Stanje.V_TEKU) {
				expandNode(promisingNode);
			}
			Node nodeToExplore = promisingNode;
			if (promisingNode.childArray.size() > 0) {
				nodeToExplore = promisingNode.randomChild();
			}
			Stanje playoutResult = simulatePlayout(nodeToExplore);
			backPropagation(nodeToExplore, playoutResult);
			
			i++;
		}
		System.out.println(i);
				
		Node winnerNode = root.bestChild();
		tree.root = winnerNode;
		return winnerNode.state.board.odigranePoteze.getLast().getKoordinati();
	}

	private void backPropagation(Node node, Stanje playoutResult) {
		Node tempNode = node;
		while (tempNode != null) {
			tempNode.state.visitCount++;
			if (tempNode.state.board.naPotezi.zmaga() == playoutResult) {
				tempNode.state.winScore -= WIN_SCORE;
			}
			else if (tempNode.state.board.naPotezi.nasprotnik().zmaga() == playoutResult) {
				tempNode.state.winScore += WIN_SCORE;
			}
			tempNode = tempNode.parent;
		}
	}

	private Stanje simulatePlayout(Node node) {
		Node tempNode = new Node(node);
		State tempState = tempNode.state;
		Stanje status = tempState.board.trenutnoStanje;
		if (status == tempState.board.naPotezi.nasprotnik().zmaga()) {
			node.state.winScore = Integer.MAX_VALUE / 2;
			return status;
		}
		else if (status == tempState.board.naPotezi.zmaga()) {
			node.state.winScore = Integer.MIN_VALUE / 2;
			return status;
		}
		while (status == Stanje.V_TEKU) {
			/*
			for (Koordinati p : tempState.board.moznePoteze()) {
				tempState.board.odigraj(p);
				if (tempState.board.trenutnoStanje != Stanje.V_TEKU) {
					return tempState.board.trenutnoStanje;
				}
				else {
					tempState.board.razveljaviZadnjo();
				}
			}
			*/
			tempState.randomPlay();
			status = tempState.board.trenutnoStanje;
		}
		return status;
	}

	private void expandNode(Node node) {
		List<State> possibleStates = node.state.getAllPossibleStates();
		for (State s : possibleStates) {
			Node newNode = new Node(s);
			newNode.parent = node;
			node.childArray.add(newNode);
		}
	}

	private Node selectPromisingNode(Node root) {
		Node node = root;
		while (node.childArray.size() != 0) {
			node = UCT.findBestNodeWithUCT(node);
		}
		return node;
	}
}
