public enum Igralec {
	C, B;

	public Igralec nasprotnik() {
		return (this == C ? B : C);
	}

	public Polje getPolje() {
		return (this == C ? Polje.C : Polje.B);
	}
    public Stanje zmaga(){
        return (this == C ? Stanje.ZMAGA_C : Stanje.ZMAGA_B)
    }
}