//  Heavily inspired by the work at https://github.com/suragnair/alpha-zero-general

package montecarlo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


import splosno.Pair;
import splosno.Utils;

public class MonteCarloTreeSearch {
	
	protected Game igra;
	protected NNet nnet;
	
	private final int timeMilli = 1000;
	private final double cpuct = 1.0;
	private final double EPS = 1e-8;
	
	protected Map<Pair<String, Integer>, Double> Qsa;
	protected Map<Pair<String, Integer>, Integer> Nsa;
	protected Map<String, Integer> Ns;
	protected Map<String, Double> Es;
	protected Map<String, double[]> Ps;
	protected Map<String, int[]> Vs;
	
	private int depth;
	
	public MonteCarloTreeSearch(Game igra, NNet nnet) {
		this.igra = igra;
		this.nnet = nnet;
		Qsa = new HashMap<Pair<String, Integer>, Double>();
		Nsa = new HashMap<Pair<String, Integer>, Integer>();
		Ns = new HashMap<String, Integer>();
		Es = new HashMap<String, Double>();
		Ps = new HashMap<String, double[]>();
		Vs = new HashMap<String, int[]>();
		depth = 0;
	}
	
	private long calcDepth(String s) {
		return s.chars().filter(c -> c == '1').count();
	}
	
	public void cleanupMaps() {
		Qsa.keySet().removeIf(e -> calcDepth(e.getFirst()) < depth);
		Nsa.keySet().removeIf(e -> calcDepth(e.getFirst()) < depth);
		Ns.keySet().removeIf(e -> calcDepth(e) < depth);
		Es.keySet().removeIf(e -> calcDepth(e) < depth);
		Ps.keySet().removeIf(e -> calcDepth(e) < depth);
		Vs.keySet().removeIf(e -> calcDepth(e) < depth);
	}
	
	public double[] getActionProb(Board board) {
		return getActionProb(board, 1);
	}
	
	public double[] getActionProb(Board board, double temp) {
		depth += 1;
		long start = System.currentTimeMillis();
		int n = 0;
		while (start + timeMilli > System.currentTimeMillis()) {
			search(board);
			n++;
		}
		System.out.println(n + " simulacij");
		
		String s = igra.stringRepresentation(board);
		int[] counts = new int[igra.getActionSize()];
		
		for (int i = 0; i < igra.getActionSize(); ++i) {
			Pair<String, Integer> sa = new Pair<String, Integer>(s, i);
			counts[i] = Nsa.getOrDefault(sa, 0);
		}
		
		cleanupMaps();
		
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
		
		if (!Es.containsKey(s)) {
			Es.put(s, igra.getGameEnded(board, 1));
		}
		if (Es.get(s) != 0) {
			return -Es.get(s);
		}
		if (!Ps.containsKey(s)) {
			Pair<double[], Double> result = nnet.predict(board);
			Ps.put(s, result.getFirst());
			double v = result.getSecond();
			
			int[] valids = igra.getValidMoves(board, 1);
			double[] arr = Ps.get(s);
			for (int i = 0; i < arr.length; ++i) {
				arr[i] = valids[i] == 1 ? arr[i] : 0;
			}
			double sum = Utils.sumDoubleArray(arr);
			if (sum > 0) {
				for (int i = 0; i < arr.length; ++i) {
					arr[i] = arr[i] / sum;
				}
				Ps.replace(s, arr);
			}
			else {
				System.out.println("Nekaj ni cisto vredu z nnet policy - veljavne poteze so vse 0");
				int vSum = Utils.sumIntArray(valids);
				double[] newArr = new double[valids.length];
				for (int i = 0; i < valids.length; ++i) {
					newArr[i] = valids[1] / vSum;
				}
				Ps.replace(s, newArr);
			}
			
			Vs.put(s, valids);
			Ns.put(s, 0);
			return -v;
		}

		int[] valids = Vs.get(s);
		double curBest = -Double.MAX_VALUE;
		int bestAction = -1;
		
		
		for (int a = 0; a < igra.getActionSize(); ++a) {
			if (valids[a] == 1) {
				double u = 0;
				Pair<String, Integer> p = new Pair<String, Integer>(s, a);
				if (Qsa.containsKey(p)) {
					u = Qsa.get(p) + cpuct * Ps.get(s)[a] * Math.sqrt(Ns.get(s)) / (1 + Nsa.get(p));
				}
				else {
					u = cpuct * Ps.get(s)[a] * Math.sqrt(Ns.get(s) + EPS);
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
		int nextPlayer = result.getSecond();
		nextBoard = igra.getCannonicalForm(nextBoard, nextPlayer);
		
		double v = search(nextBoard);
		
		Pair<String, Integer> bestCombo = new Pair<String, Integer>(s, a);
		if (Qsa.containsKey(bestCombo)) {
			Qsa.put(bestCombo, (Nsa.get(bestCombo) * Qsa.get(bestCombo) + v) / (Nsa.get(bestCombo) + 1));
			Nsa.put(bestCombo, Nsa.get(bestCombo) + 1);
		}
		else {
			Qsa.put(bestCombo, v);
			Nsa.put(bestCombo, 1);
		}
		Ns.put(s, Ns.get(s) + 1);
		return -v;
	}
	
}
