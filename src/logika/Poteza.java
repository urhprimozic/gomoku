package logika;

public class Poteza {
	private splosno.Koordinati p;
	private Igralec i;
	
	public Poteza(int x, int y, Igralec i) {
		this.p = new splosno.Koordinati(x, y);
		this.i = i;
	}
	
	public splosno.Koordinati getKoordinati() {return p;}
	
	public Igralec getIgralec() {return i;}
	
}
