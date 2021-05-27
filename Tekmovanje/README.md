Ekstra stvari, potrebne za delovanje nevronske mreže

* .jar datoteke v ExternalJAR se samo dodajo v Eclipsu pod Java Build Path : Add External JARs
* Za GomokuNNet.pt je trenutno mišljeno, da je v top level mapi, sicer se da to spremeniti v
inteligenca/NNet.java, kjer se v konstruktorju spremeni relativna pot.
* Nalaganje nevronske mreže iz datoteke zna trajati, nalaga se pa jasno samo ob instanciiranju novega NNet objekta.
