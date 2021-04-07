package gui;

import javax.swing.*;

import java.awt.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;

@SuppressWarnings("serial")
public class Platno extends JPanel implements MouseListener, MouseMotionListener {

	public Platno(int visina, int sirina) {
		this.setPreferredSize(new Dimension(visina, sirina));
		this.addMouseListener(this);
		this.addMouseMotionListener(this);
	}


	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g); 
		//this.repaint();
	}

	@Override
	public void mouseClicked(MouseEvent e) {
		System.out.println("Mouse clicked");
	}

	@Override
	public void mousePressed(MouseEvent e) {
		System.out.println("Mouse pressed");
	}

	@Override
	public void mouseReleased(MouseEvent e) {
		System.out.println("Mouse released");

	}

	@Override
	public void mouseEntered(MouseEvent e) {
		System.out.println("Mouse entered");
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		System.out.println("Mouse dragged");
	}

	@Override
	public void mouseExited(MouseEvent e) {
		System.out.println("Mouse exited");
	}

	@Override
	public void mouseMoved(MouseEvent arg0) {
		// TODO Auto-generated method stub
		System.out.println("Mouse moved");

	}
}
