package inteligenca;

public class MCTSMapEntry {
	public int N;
	public double E;
	public int[] V;
	public double[] P;
	
	public MCTSMapEntry() {
		this.N = Integer.MIN_VALUE;
		this.E = -Double.MIN_VALUE;
		this.V = null;
		this.P = null;
	}
	
	public MCTSMapEntry(int N, double E, int[] V, double[] P) {
		this.N = N;
		this.E = E;
		this.V = V;
		this.P = P;
	}
}
