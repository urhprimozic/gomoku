import logika.Igra;
import logika.Stanje;

import java.util.Scanner;

//Game loop in to

public class Gomoku {
    public static void main(String[] args) {
    	
    	Scanner in = new Scanner(System.in);
    	game_loop:
        while (true) {
        	Igra igra = new Igra(7, 7);
        	
        	int i = 0;
        	
        	inner_loop:
        	while (true) {
        		++i;
        		igra.odigrajNakljucnoPotezo();
            	System.out.println(igra);
            	
            	System.out.print(i + " ");
            	System.out.println(igra.trenutnoStanje);
            	splosno.Koordinati zadnja = igra.odigranePoteze.getLast().getKoordinati();
            	System.out.println("(" + (zadnja.getX() + 1) + ", " + (zadnja.getY() + 1) + ") " + igra.naPotezi.nasprotnik());
            	System.out.println("---------------------------------------------");
            	if (igra.trenutnoStanje != Stanje.V_TEKU) {
            		System.out.println("Ponovi igro? [D/N]");
            		String s = in.nextLine();
            		
            		if (s.equals("N")) {
            			break game_loop;
            		}
            		else {
            			break inner_loop;
            		}
            	}        	
        	}       	
        }
        in.close();
                
    }
}
