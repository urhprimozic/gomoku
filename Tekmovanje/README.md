Ekstra stvari, potrebne za delovanje nevronske mreže

* .jar datoteke v ExternalJAR se samo dodajo v Eclipsu pod Java Build Path : Add External JARs
* Nevronska mreža je prevelika za Github (cca 130MB), zato je na voljo [tukaj](https://drive.google.com/file/d/16MdSD9MrXKQqXPTWkMArrID-27b_VOom/view?usp=sharing). Ime datoteke je GomokuNNet.pt.
* Za GomokuNNet.pt je trenutno mišljeno, da je v top level mapi, sicer se da to spremeniti v
inteligenca/NNet.java, kjer se v konstruktorju spremeni relativna pot.
* Nalaganje nevronske mreže iz datoteke zna trajati, nalaga se pa jasno samo ob instanciiranju novega NNet objekta.
