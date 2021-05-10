package logika;


import splosno.Koordinati;

public class Game {
	public static final int nir = 5;
	
	public static String stringRepresentation(Board b) {
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < b.n; ++i) {
			for (int j = 0; j < b.n; ++j) {
				sb.append(Integer.toString(b.plosca[i][j]));
			}
		}
		return sb.toString();
	}
	
	public static int[][] getInitBoard(int size) {
		Board b = new Board(size);
		return b.plosca;
	}
	
	public static Pair<Integer, Integer> getBoardSize(Board b) {
		return new Pair<Integer, Integer>(b.n, b.n);
	}
	
	public static int getActionSize(Board b) {
		return b.n * b.n;
	}
	
	public static Pair<Board, Integer> getNextState(Board b, int p, int a) {
		Board next = new Board(b.n);
		next.plosca = new int[b.n][b.n];
		for (int i = 0; i < b.n; ++i) {
			for (int j = 0; j < b.n; ++j) {
				next.plosca[i][j] = b.plosca[i][j];
			}
		}
		next.executeMove(new Koordinati(a / b.n, a % b.n), p);
		return new Pair<Board, Integer>(next, -p);
	}
	
	public static int[] getValidMoves(Board b, int p) {
		int[] valids = new int[getActionSize(b)];
		for (int i = 0; i < b.n; ++i) {
			for (int j = 0;  j < b.n; ++j) {
				valids[b.n * i + j] = b.plosca[i][j] == 0 ? 1 : 0;
			}
		}
		return valids;
	}
	
	public static double getGameEnded(Board b, int player) {
		for (int w = 0; w < b.n; ++w) {
			for (int h = 0; h < b.n; ++h) {
				if_1:
				if (w < b.n - nir + 1 && b.plosca[w][h] != 0) {
					int color = b.plosca[w][h];
					for (int i = w; i < w + nir; ++i) {
						if (b.plosca[i][h] != color) {
							break if_1;
						}
					} 
					return color;
				}
				
				if_2:
				if (h < b.n - nir + 1 && b.plosca[w][h] != 0) {
					int color = b.plosca[w][h];
					for (int j = h; j < h + nir; ++j) {
						if (b.plosca[w][j] != color) {
							break if_2;
						}
					}
					return color;
				}
				
				if_3:
				if (w < b.n - nir + 1 && h < b.n - nir + 1 && b.plosca[w][h] != 0) {
					int color = b.plosca[w][h];
					for (int k = 0; k < nir; ++k) {
						if (b.plosca[w+k][h+k] != color) {
							break if_3;
						}
					}
					return color;
				}
				
				if_4:
				if (w < b.n - nir + 1 && h < b.n && h >= nir - 1 && b.plosca[w][h] != 0) {
					int color = b.plosca[w][h];
					for (int l = 0; l < nir; ++l) {
						if (b.plosca[w+l][h-l] != color) {
							break if_4;
						}
					}
					return color;
				}
			}
		}
		for (int[] row : b.plosca) {
			for (int c : row) {
				if (c == 0) {
					return 0;
				}
			}
		}
		return 1e-4;
	}
	
	public static Board getCannonicalForm(Board b, int player) {
		for (int i = 0; i < b.n; ++i) {
			for(int j = 0; j < b.n; ++j) {
				b.plosca[i][j] *= player;
			}
		}
		return b;
	}
}

