
public class Poteza {
	private Koordinati p;
	private Igralec i;
	
	public Poteza(int x, int y, Igralec i) {
		this.p = new Koordinati(x, y);
		this.i = i;
	}
	
	public Koordinati getKoordinati() {return p;}
	
	public Igralec getIgralec() {return i;}
	
}
