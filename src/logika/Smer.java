package logika;
// To bi lahko zamenjali s koordinato..
/// TODO
/*
namesto tuplov (0,1), (1,0), (1,1)
*/

public class Smer {
    public int x;
    public int y;

    public Smer(int x, int y){
        this.x = x;
        this.y = y;
    }

    static Smer dol(){
        return new Smer(0, 1);
    }
    static Smer desno(){
        return new Smer(1, 0);
    }
    static Smer desnoDol(){
        return new Smer(1, 1);
    }
}
