package montecarlo;

import java.util.ArrayList;
import java.util.List;


import splosno.Koordinati;

public class Board {
	public int n;
	public int[][] plosca;
	
	public Board(int n) {
		this.n = n;
		plosca = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                plosca[i][j] = 0;
            }
        }
	}
	
	public List<Koordinati> getLegalMoves() {
        List<Koordinati> poteze = new ArrayList<splosno.Koordinati>();
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (plosca[i][j] == 0)
                    poteze.add(new splosno.Koordinati(i, j));
        return poteze;
    }
	
	public void executeMove(Koordinati t, int p) {
		plosca[t.getX()][t.getY()] = p;
	}
}
