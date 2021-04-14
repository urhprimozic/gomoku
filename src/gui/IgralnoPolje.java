package gui;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

import javax.swing.JPanel;

import logika.Igra;
import logika.Polje;
import splosno.Koordinati;
import vodja.Vodja;

/**
 * Pravokotno območje, v katerem je narisano igralno polje.
 */
@SuppressWarnings("serial")
public class IgralnoPolje extends JPanel implements MouseListener {

	// Relativna širina črte
	private final static double SIRINA_CRTE = 0.08;
	// Velikost zetona, relativna na kvadratek
	private final static double VELIKOST_ZETONA = 0.9;
	// Barva črt v mreži
	private Color barvaCrte;
	private Color barvaC;
	private Color barvaB;

	public IgralnoPolje() {
		setBackground(Color.WHITE);
		this.addMouseListener(this);
		barvaCrte = Color.BLACK;
		barvaC = Color.BLACK;
		barvaB = Color.WHITE;
	}

	// Širina enega kvadratka
	private double squareWidth() {
		Igra igra = Vodja.igra;
		if (igra == null)
			return 0.0;
		return Math.min(getWidth() / igra.sirina, getHeight() / igra.visina);
	}

	@Override
	public Dimension getPreferredSize() {
		return new Dimension(600, 600);
	}

	// Relativni prostor okoli X in O
	private final static double PADDING = 0.18;

	/**
	 * V grafični kontekst g2 nariši križec v polje (i,j)
	 * 
	 * @param g2
	 * @param i
	 * @param j
	 */
	private void paintX(Graphics2D g2, int i, int j) {
		double w = squareWidth();
		double r = w * (1.0 - SIRINA_CRTE - 2.0 * PADDING); // sirina X
		double x = w * (i + 0.5 * SIRINA_CRTE + PADDING);
		double y = w * (j + 0.5 * SIRINA_CRTE + PADDING);
		g2.setColor(Color.BLUE);
		g2.setStroke(new BasicStroke((float) (w * SIRINA_CRTE)));
		g2.drawLine((int) x, (int) y, (int) (x + r), (int) (y + r));
		g2.drawLine((int) (x + r), (int) y, (int) x, (int) (y + r));
	}

	/**
	 * V grafični kontekst {@g2} nariši križec v polje {@(i,j)}
	 * 
	 * @param g2
	 * @param i
	 * @param j
	 */
	private void paintO(Graphics2D g2, int i, int j) {
		double w = squareWidth();
		double d = w * (1.0 - SIRINA_CRTE - 2.0 * PADDING); // premer O
		double x = w * (i + 0.5 * SIRINA_CRTE + PADDING);
		double y = w * (j + 0.5 * SIRINA_CRTE + PADDING);
		g2.setColor(Color.RED);
		g2.setStroke(new BasicStroke((float) (w * SIRINA_CRTE)));
		g2.drawOval((int) x, (int) y, (int) d, (int) d);
	}

	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g);
		Graphics2D g2 = (Graphics2D) g;

		Igra igra = Vodja.igra;
		double w = squareWidth();
		if (igra != null) {
			g2.setStroke(new BasicStroke((float) (w * SIRINA_CRTE)));

			// polja
			for (int vrstica = 0; vrstica < igra.visina; vrstica++) {
				for (int stolpec = 0; stolpec < igra.sirina; stolpec++) {
					Polje p = igra.plosca[vrstica][stolpec];
					if (p == Polje.PRAZNO)
						continue;
					if (p == Polje.C)
						g2.setColor(barvaC);
					if (p == Polje.B)
						g2.setColor(barvaB);
					g2.drawOval((int) (stolpec * w + (VELIKOST_ZETONA / 2)), (int)(vrstica * w + (VELIKOST_ZETONA / 2)),
							(int)(w * VELIKOST_ZETONA),(int) (w * VELIKOST_ZETONA));
				}
			}

			// mreža
			g2.setColor(barvaCrte);
			for (int vrstica = 0; vrstica < igra.visina; vrstica++) {
				g2.drawLine(0, vrstica * (int) w, igra.sirina, vrstica * (int) w);
			}
			for (int stolpec = 0; stolpec < igra.sirina; stolpec++) {
				g2.drawLine(stolpec * (int) w, 0, stolpec * (int) w, igra.visina);
			}
		}

	}

	@Override
	public void mouseClicked(MouseEvent e) {

	}

	@Override
	public void mousePressed(MouseEvent e) {
	}

	@Override
	public void mouseReleased(MouseEvent e) {
	}

	@Override
	public void mouseEntered(MouseEvent e) {
	}

	@Override
	public void mouseExited(MouseEvent e) {
	}

}
