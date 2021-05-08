# Povzeto po: https://github.com/suragnair/alpha-zero-general
from gomoku import Gomoku
from logika import Stanje
import logging

from tqdm import tqdm

from logika import Stanje

log = logging.getLogger(__name__)


class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, igralec1, igralec2, igra, izpis = None) -> None:
        '''
        TODO komentarji
        '''
        self.igralec1 = igralec1
        self.igralec2 = igralec2
        self.igra = igra 
        self.izpis = izpis
    def odigrajIgre(self, n, verbose=False):
        '''
        Odigra 2n iger, v n igrah je igralec1 bel, v n igral pa igralec 2

        Parameter
        ---------
            n (int) - število iger

        Returns
        ---------
            (#iger, kjer zmaga 1, ..zmaga 2, ..neodločeno)
        '''
        st_zmaga1 = 0
        st_zmaga2 = 0
        st_neoldoceno = 0
        gomoku = Gomoku()
        for _ in tqdm(range(n), desc='Arena.odigrajIgre: Igralec_1', total=n):
            #odigramo n iger, kjer začne igralec1
            rezultat = gomoku.odigraj_igro(self.igralec1, self.igralec2)
            if rezultat == Stanje.ZMAGA_C:
                st_zmaga1 += 1
            elif rezultat == Stanje.ZMAGA_B:
                st_zmaga2 += 1
            else: 
                st_neoldoceno += 1
        for _ in tqdm(range(n), desc='Arena.odigrajIgre: Igralec_2', total=n):
            #odigramo n iger, kjer začne igralec1
            rezultat = gomoku.odigraj_igro(self.igralec2, self.igralec1)
            if rezultat == Stanje.ZMAGA_C:
                st_zmaga2 += 1
            elif rezultat == Stanje.ZMAGA_B:
                st_zmaga1 += 1
            else: 
                st_neoldoceno += 1
        
        return st_zmaga1, st_zmaga2, st_neoldoceno
        
        
