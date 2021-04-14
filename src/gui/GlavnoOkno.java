package gui;

import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.EnumMap;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

import vodja.Vodja;
import vodja.VrstaIgralca;
import logika.Igralec;


/**
 * Glavno okno aplikacije hrani trenutno stanje igre in nadzoruje potek
 * igre.
 * 
 * @author AS
 *
 */
@SuppressWarnings("serial")
public class GlavnoOkno extends JFrame implements ActionListener {
	/**
	 * JPanel, v katerega igramo
	 */
	private IgralnoPolje polje;

	
	//Statusna vrstica v spodnjem delu okna
	private JLabel status;
	
	// Izbire v menujih
	private JMenuItem igraClovekRacunalnik;
	private JMenuItem igraRacunalnikClovek;
	private JMenuItem igraClovekClovek;
	private JMenuItem igraRacunalnikRacunalnik;

	/**
	 * Ustvari novo glavno okno in prični igrati igro.
	 */
	public GlavnoOkno() {
		
		this.setTitle("Gomoku");
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
		this.setLayout(new GridBagLayout());
	
		// menu
		JMenuBar menu_bar = new JMenuBar();
		this.setJMenuBar(menu_bar);
		// Nova igra
		JMenu igra_menu = new JMenu("Nova igra TODO");
		menu_bar.add(igra_menu);


		igraClovekRacunalnik = new JMenuItem("Človek – računalnik");
		igra_menu.add(igraClovekRacunalnik);
		igraClovekRacunalnik.addActionListener(this);
		
		igraRacunalnikClovek = new JMenuItem("Računalnik – človek");
		igra_menu.add(igraRacunalnikClovek);
		igraRacunalnikClovek.addActionListener(this);
		
		igraClovekClovek = new JMenuItem("Človek – človek");
		igra_menu.add(igraClovekClovek);
		igraClovekClovek.addActionListener(this);
		
		igraRacunalnikRacunalnik = new JMenuItem("Računalnik – računalnik");
		igra_menu.add(igraRacunalnikRacunalnik);
		igraRacunalnikRacunalnik.addActionListener(this);

		//nastavitve
		JMenu nastavitve_menu = new JMenu("Nastavitve-TODO");
		menu_bar.add(nastavitve_menu);

		

		// igralno polje
		polje = new IgralnoPolje();

		GridBagConstraints polje_layout = new GridBagConstraints();
		polje_layout.gridx = 0;
		polje_layout.gridy = 0;
		polje_layout.fill = GridBagConstraints.BOTH;
		polje_layout.weightx = 1.0;
		polje_layout.weighty = 1.0;
		getContentPane().add(polje, polje_layout);
		
		// statusna vrstica za sporočila
		status = new JLabel();
		status.setFont(new Font(status.getFont().getName(),
							    status.getFont().getStyle(),
							    20));
		GridBagConstraints status_layout = new GridBagConstraints();
		status_layout.gridx = 0;
		status_layout.gridy = 1;
		status_layout.anchor = GridBagConstraints.CENTER;
		getContentPane().add(status, status_layout);
		
		status.setText("Izberite igro!");
		
	}
	
	
	@Override
	public void actionPerformed(ActionEvent e) {
		// if (e.getSource() == igraClovekRacunalnik) {
		// 	Vodja.vrstaIgralca = new EnumMap<Igralec,VrstaIgralca>(Igralec.class);
		// 	Vodja.vrstaIgralca.put(Igralec.O, VrstaIgralca.C); 
		// 	Vodja.vrstaIgralca.put(Igralec.X, VrstaIgralca.R);
		// 	Vodja.igramoNovoIgro();
		// } else if (e.getSource() == igraRacunalnikClovek) {
		// 	Vodja.vrstaIgralca = new EnumMap<Igralec,VrstaIgralca>(Igralec.class);
		// 	Vodja.vrstaIgralca.put(Igralec.O, VrstaIgralca.R); 
		// 	Vodja.vrstaIgralca.put(Igralec.X, VrstaIgralca.C);
		// 	Vodja.igramoNovoIgro();
		// } else if (e.getSource() == igraClovekClovek) {
		// 	Vodja.vrstaIgralca = new EnumMap<Igralec,VrstaIgralca>(Igralec.class);
		// 	Vodja.vrstaIgralca.put(Igralec.O, VrstaIgralca.C); 
		// 	Vodja.vrstaIgralca.put(Igralec.X, VrstaIgralca.C);
		// 	Vodja.igramoNovoIgro();
		// } else if (e.getSource() == igraRacunalnikRacunalnik) {
		// 	Vodja.vrstaIgralca = new EnumMap<Igralec,VrstaIgralca>(Igralec.class);
		// 	Vodja.vrstaIgralca.put(Igralec.O, VrstaIgralca.R); 
		// 	Vodja.vrstaIgralca.put(Igralec.X, VrstaIgralca.R);
		// 	Vodja.igramoNovoIgro();
		// }
	}

	public void osveziGUI() {
		// if (Vodja.igra == null) {
		// 	status.setText("Igra ni v teku.");
		// }
		// else {
		// 	switch(Vodja.igra.stanje()) {
		// 	case NEODLOCENO: status.setText("Neodločeno!"); break;
		// 	case V_TEKU: 
		// 		status.setText("Na potezi je " + Vodja.igra.naPotezi + 
		// 				" - " + Vodja.vrstaIgralca.get(Vodja.igra.naPotezi)); 
		// 		break;
		// 	case ZMAGA_O: 
		// 		status.setText("Zmagal je O - " + 
		// 				Vodja.vrstaIgralca.get(Igralec.O));
		// 		break;
		// 	case ZMAGA_X: 
		// 		status.setText("Zmagal je X - " + 
		// 				Vodja.vrstaIgralca.get(Igralec.X));
		// 		break;
		// 	}
		// }
		polje.repaint();
	}
	



}
