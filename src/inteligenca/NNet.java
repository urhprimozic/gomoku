package inteligenca;

import logika.Board;
import logika.Pair;

public class NNet {
	
	public Pair<double[], Double> predict(Board b) {
		double[] arr = new double[b.n * b.n];
		for (int i = 0; i < arr.length; ++i) {
			arr[i] = Math.random();
		}
		return new Pair<double[], Double>(arr, 2*Math.random() - 1);
	}
}
