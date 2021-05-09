//  Heavily inspired by the work at https://github.com/suragnair/alpha-zero-general

package inteligenca;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import logika.Board;
import logika.Game;
import logika.Pair;
import logika.Utils;

public class MonteCarloTreeSearch {
	
	protected Game igra;
	protected NNet nnet;
	
	private final int timeMilli = 5000;
	private final double cpuct = 1.0;
	private final double EPS = 1e-8;
		
	protected Map<Pair<String, Integer>, Pair<Double, Integer>> stateActionMap;
	protected Map<String, MCTSMapEntry> stateMap;
	
	private int depth;
	private int gamePlayer;
	
	public MonteCarloTreeSearch(Game igra, NNet nnet, int p) {
		this.igra = igra;
		this.nnet = nnet;
		this.gamePlayer = p;
		
		stateActionMap = new HashMap<Pair<String, Integer>, Pair<Double, Integer>>();
		stateMap = new HashMap<String, MCTSMapEntry>();
		depth = 0;
	}
	
	private long calcDepth(String s) {
		return s.chars().filter(c -> c == '1').count() / 2 + 1;
	}
	
	public void pruneTree() {
		stateActionMap.keySet().removeIf(e -> calcDepth(e.getFirst()) < depth);
		stateMap.keySet().removeIf(e -> calcDepth(e) < depth);
	}
	
	public double[] getActionProb(Board board) {
		return getActionProb(board, 1);
	}
	
	public double[] getActionProb(Board board, double temp) {
		
		Board canonicalBoard = new Board(igra.n);
		for (int i = 0; i < igra.n; ++i) {
			for (int j = 0; j < igra.n; ++j) {
				canonicalBoard.plosca[i][j] = board.plosca[i][j] * -gamePlayer;
			}
		}		
		
		depth += 1;
		long start = System.currentTimeMillis();
		int n = 0;
		while (start + timeMilli > System.currentTimeMillis()) {
//		while (n < 10000) {
			search(canonicalBoard);
			n++;
		}
		System.out.println(n + " simulacij");
		
		String s = igra.stringRepresentation(canonicalBoard);
		int[] counts = new int[igra.getActionSize()];
		
		for (int i = 0; i < igra.getActionSize(); ++i) {
			Pair<String, Integer> sa = new Pair<String, Integer>(s, i);
			Pair<Double, Integer> entry = stateActionMap.get(sa);
			counts[i] = entry == null ? 0 : entry.getLast();
		}
		
		pruneTree();
		
		if (temp == 0) {
			int bestInts = Utils.maxInIntArray(counts);
			List<Integer> best = new ArrayList<Integer>();
			for (int x : counts) {
				if (x == bestInts) {
					best.add(x);
				}
			}
			
			double[] probs = new double[counts.length];
			int x = best.get((int) (Math.random() * best.size()));
			for (int i = 0; i < counts.length; ++i) {
				probs[i] = i == x ? x : i;
			}
			return probs;
		}
		
		double[] probs = new double[counts.length];
		int sum = Utils.sumIntArray(counts);
		
		for (int i = 0; i < counts.length; ++i) {
			double x = Math.pow(counts[i], 1. / temp);
			probs[i] = x / sum;
		}
		return probs;
	}
	
	public double search(Board board) {
		String s = igra.stringRepresentation(board);
		
		MCTSMapEntry entry = stateMap.get(s);
		
		if (entry == null) {
			entry = new MCTSMapEntry();
			stateMap.put(s, entry);
		}
		
		if (entry.E == -Double.MIN_VALUE) {
			entry.E = igra.getGameEnded(board, 1);
		}
		if (entry.E != 0) {
			return -entry.E;
		}
		if (entry.P == null) {
			Pair<double[], Double> result = nnet.predict(board);
			entry.P = result.getFirst();
			double v = result.getLast();
			
			int[] valids = igra.getValidMoves(board, 1);
			double[] arr = entry.P;
			for (int i = 0; i < arr.length; ++i) {
				arr[i] = valids[i] == 1 ? arr[i] : 0;
			}
			double sum = Utils.sumDoubleArray(arr);
			if (sum > 0) {
				for (int i = 0; i < arr.length; ++i) {
					arr[i] = arr[i] / sum;
				}
				entry.P = arr;
			}
			else {
				System.out.println("Nekaj ni cisto vredu z nnet policy - veljavne poteze so vse 0");
				int vSum = Utils.sumIntArray(valids);
				double[] newArr = new double[valids.length];
				for (int i = 0; i < valids.length; ++i) {
					newArr[i] = valids[1] / vSum;
				}
				entry.P = newArr;
			}
			
			entry.V = valids;
			entry.N = 0;
			return -v;
		}

		int[] valids = entry.V;
		double curBest = -Double.MAX_VALUE;
		int bestAction = -1;
		
		
		for (int a = 0; a < igra.getActionSize(); ++a) {
			if (valids[a] == 1) {
				double u = 0;
				Pair<String, Integer> p = new Pair<String, Integer>(s, a);
				Pair<Double, Integer> saVal = stateActionMap.get(p);
				
				if (saVal != null) {
					double QVal = saVal.getFirst();
					int NVal = saVal.getLast();
					u = QVal + cpuct * entry.P[a] * Math.sqrt(entry.N) / (1 + NVal);
				}
				else {
					u = cpuct * entry.P[a] * Math.sqrt(entry.N + EPS);
				}
				if (u > curBest) {
					curBest = u;
					bestAction = a;
				}
			}
		}
		
		int a = bestAction;
		
		Pair<Board, Integer> result = igra.getNextState(board, 1, a);
		Board nextBoard = result.getFirst();
		int nextPlayer = result.getLast();
		nextBoard = igra.getCannonicalForm(nextBoard, nextPlayer);
		
		double v = search(nextBoard);
		
		Pair<String, Integer> bestCombo = new Pair<String, Integer>(s, a);
		Pair<Double, Integer> saVal = stateActionMap.get(bestCombo);
		
		if (saVal != null) {
			double QVal = saVal.getFirst();
			int NVal = saVal.getLast();
			
			saVal.setFirst((NVal * QVal + v) / (NVal + 1));
			saVal.setLast(NVal + 1);
		}
		else {
			stateActionMap.put(bestCombo, new Pair<Double, Integer>(v, 1));
		}
		entry.N += 1;
		return -v;
	}
	
}
