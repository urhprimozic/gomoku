import logika.Igra;
import logika.Stanje;

import java.util.Scanner;

//Game loop in to

public class Gomoku {
    public static void main(String[] args) {
    	
    	Scanner in = new Scanner(System.in);
    	
        while (true) {
        	Igra igra = new Igra();
        	
        	igra.odigrajNakljucnoPotezo();
        	System.out.println(igra);
        	
        	if (igra.stanje() != Stanje.V_TEKU) {
        		System.out.println("Ponovi igro? [D/N]");
        		String s = in.nextLine();
        		
        		if (s.equals("N")) {
        			break;
        		}
        	}        	
        }
                
    }
}
