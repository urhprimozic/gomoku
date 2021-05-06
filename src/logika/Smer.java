package logika;
// To bi lahko zamenjali s koordinato..
/// TODO
/*
namesto tuplov (0,1), (1,0), (1,1)
*/

public class Smer {
    public int x;
    public int y;

    public static Smer DOL;
    public static Smer DESNO_DOL;
    public static Smer DESNO;
    public static Smer DESNO_GOR;

    public Smer(int x, int y){
        this.x = x;
        this.y = y;
    }

    static {
        DOL = new Smer (1, 0);
        DESNO_DOL = new Smer(1, 1);
        DESNO = new Smer(0, 1);
        DESNO_GOR = new Smer(1, -1);
    };
}
