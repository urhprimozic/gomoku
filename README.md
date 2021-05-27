# Gomoku
Igra Gomoku z umetno inteligenco. Projekt pri Programiranju 2 na FMF.


_Gomoku game with simple AI. Project for programming 2  on FMF._

## Avtorja
- [Jon Mikoš](https://github.com/MikosJon)
- [Urh Primožič](https://github.com/urhprimozic/)


### Uporaba
Igro se požene iz datoteke **Gomoku.java**. Odpre se grafični vmesnik. Na vrhu ima orodno vrstico, kjer lahko začnemo novo igro ali spremenimo nastavitve.

Ker je nevronska mreža prevelika za github, je na voljo [tukaj](https://drive.google.com/file/d/1AG9Fzl50kVIEeXK6yySTa0QZbDWp38lI/view). Dobljena datoteka naj bo shranjena v top level mapi.
## Umetna inteligenca

Uporabljava Monte Carlo Tree Search z nevronsko mrežo.

Sistem za učenje je spisan v pythonu in temelji na [Alpha Zero General](https://github.com/suragnair/alpha-zero-general), a je prilagojen za delo na večih procesorjih. Vsako iteracijo učenja agent (MCTS z nevronsko mrežo) odigra *N* iger sam s seboj. Nato popravi mrežo glede na podatke, in odigra *m* iger s staro mrežo, da se odloči, ali so novi popravki dobri *(Glej vire)*.

### Uporaba
V [args.py](https://github.com/urhprimozic/gomoku/blob/main/ai/args.py) nastavi parametre za učenje in poženi [eval.sh](https://github.com/urhprimozic/gomoku/blob/main/ai/eval.sh). Za najino UI sva uporabila spodnje parametre na TODO specifikacije, kolk časa.

    'numIters': 100,
    'numEps': 750,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 90000,
    'numMCTSSims': 20,
    'arenaCompare': 30,
    'cpuct': 3,
    'timeLimit' :4.9,

### Viri:
 - [Alpha Zero General](https://raw.githubusercontent.com/suragnair/alpha-zero-general/master/pretrained_models/writeup.pdf#cite.alphagozero)
 - [Adam](https://arxiv.org/pdf/1412.6980.pdf)
 - [Memory Bounded Monte Carlo Tree Search](http://orangehelicopter.com/academic/papers/powley_aiide17.pdf)
