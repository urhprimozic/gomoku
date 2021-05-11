package logika;

import splosno.Koordinati;

public class Igra {
	public final int N = 15;
	
	public Board board;
	public int igralec;
	
	public Igra() {
		board = new Board(N);
		igralec = 1;
	}
	
	public boolean odigraj(Koordinati koordinati) {
		if (board.plosca[koordinati.getX()][koordinati.getY()] == 0) {
			board.executeMove(koordinati, igralec);
			igralec *= -1;
			System.out.println(koordinati.toString());
			return true;
		}
		return false;
	}
}
