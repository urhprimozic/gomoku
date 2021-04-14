import logika.Igra;
import logika.Stanje;
import vodja.Vodja;

import java.util.Scanner;

import gui.GlavnoOkno;

//Game loop in to

public class Gomoku {

	protected void tekstovniVmesnik(){
		   	
    	Scanner in = new Scanner(System.in);
    	game_loop:
        while (true) {
        	Igra igra = new Igra(7,10);
        	
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
    public static void main(String[] args) {
		GlavnoOkno glavno_okno = new GlavnoOkno();
		glavno_okno.pack();
		glavno_okno.setVisible(true);
		Vodja.okno = glavno_okno;           
    }
}
