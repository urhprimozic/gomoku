

import gui.GlavnoOkno;
import vodja.Vodja;

//Game loop in to

public class Gomoku {

//	protected static void tekstovniVmesnik(){
//		   	
//    	Scanner in = new Scanner(System.in);
//    	game_loop:
//        while (true) {
//        	Igra igra = new Igra();
//        	
//        	int i = 0;
//        	
//        	inner_loop:
//        	while (true) {
//        		++i;
//        		igra.odigrajNakljucnoPotezo();
//            	System.out.println(igra);
//            	
//            	System.out.print(i + " ");
//            	System.out.println(igra.izracunajNovoStanje());
//            	splosno.Koordinati zadnja = igra.odigranePoteze.getLast().getKoordinati();
//            	System.out.println("(" + (zadnja.getX() + 1) + ", " + (zadnja.getY() + 1) + ") " + igra.naPotezi.nasprotnik());
//            	System.out.println("---------------------------------------------");
//            	if (igra.izracunajNovoStanje() != Stanje.V_TEKU) {
//            		System.out.println("Ponovi igro? [D/N]");
//            		String s = in.nextLine();
//            		
//            		if (s.equals("N")) {
//            			break game_loop;
//            		}
//            		else {
//            			break inner_loop;
//            		}
//            	}        	
//        	}       	
//        }
//        in.close();
//	}
	
//	protected static void mctsTest() {
//		Scanner in = new Scanner(System.in);
//		MonteCarloTreeSearch mcts = new MonteCarloTreeSearch();
//		game_loop:
//        while (true) {
//        	Igra igra = new Igra();
//        	
//        	int i = 0;
//        	
//        	inner_loop:
//        	while (true) {
//        		++i;
//        		if (igra.naPotezi == Igralec.C) {
//        			igra.odigrajNakljucnoPotezo();
//        		}
//        		else {
//        			Koordinati p = mcts.findNextMove(igra);
//        			System.out.println(p.getX() + " " + p.getY());
//        			igra.odigraj(p);
//        		}
//            	System.out.println(igra);
//            	
//            	System.out.print(i + " ");
//            	System.out.println(igra.izracunajNovoStanje());
//            	splosno.Koordinati zadnja = igra.odigranePoteze.getLast().getKoordinati();
//            	System.out.println("(" + (zadnja.getX() + 1) + ", " + (zadnja.getY() + 1) + ") " + igra.naPotezi.nasprotnik());
//            	System.out.println("---------------------------------------------");
//            	if (igra.izracunajNovoStanje() != Stanje.V_TEKU) {
//            		System.out.println("Ponovi igro? [D/N]");
//            		String s = in.nextLine();
//            		
//            		if (s.equals("N")) {
//            			break game_loop;
//            		}
//            		else {
//            			break inner_loop;
//            		}
//            	}        	
//        	}       	
//        }
//		in.close();
//	}
	
    public static void main(String[] args) {
		GlavnoOkno glavno_okno = new GlavnoOkno();
		glavno_okno.pack();
		glavno_okno.setVisible(true);
		Vodja.okno = glavno_okno;
		
		
    }
}
