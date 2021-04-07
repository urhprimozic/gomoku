package gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JFrame;


@SuppressWarnings("serial")
public class Okno extends JFrame implements ActionListener {
	@SuppressWarnings("unused")
	private Platno platno;


	public Okno(Platno platno, String ime) {
		this.platno = platno;
		this.setTitle(ime);
		this.add(platno);
		
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		// TODO

	}
}
