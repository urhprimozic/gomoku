from logika import Igra, Stanje, Igralec
from vodja import Vodja, VrstaIgralca
from Game import Game
import numpy as np


class GomokuGame(Game):
    #(vrstca, stolpec)
    DOL = (1, 0)
    DESNO = (0, 1)
    DESNO_DOL = (1, 1)
    DESNO_GOR = (-1, 1)

    def __init__(self, size):
        self.size = size
        self.actions = np.array([(i, j) for i in range(self.size)
                                 for j in range(self.size)])

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return np.array([[0 for i in range(self.size)] for i in range(self.size)])

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.size, self.size)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        if self.size ** 2 != len(self.actions):
            raise Warning(
                f'WARNING: getActionSIze() != |self.actions|!\nactions: {self.actions}')
        return self.size ** 2

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)

        Dogovor: (vrstica, stolpec)
        """
        action = self.actions[action]
        vrstica = action[0]
        stolpec = action[1]
        if board[vrstica][stolpec] == 0:  # prazno
            cpy = np.copy(board)
            cpy[vrstica][stolpec] = player
            #self.odigranePoteze.append((vrstica, stolpec, self.naPotezi))
            return (cpy, -player)
        else:
            raise Exception(
                f'ERROR in getNextState - Polje ni prazno!\nNAPAČNA POTEZA\n board:{board}\naction:{action}')

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        ans = []
        for i, j in self.actions:
            if board[i][j] == 0:
                ans.append(1)
            else:
                ans.append(0)
        return np.array(ans)

    def pet_v_vrsto(self, smer, player, zacetek, board):
        '''True, če je v dani smeri z zacetkom v 
         zacetek igralec dosegu najmanj pet zaporednih '''
        vrstica = zacetek[0]
        stolpec = zacetek[1]
        stevec = 0  # število zaporednih žetonov igralca

        while vrstica >= 0 and vrstica < self.size and stolpec >= 0 and stolpec < self.size:
            if board[vrstica][stolpec] == player:
                stevec += 1
            else:
                if stevec >= 5:
                    return True
                stevec = 0
            vrstica += smer[0]
            stolpec += smer[1]
        return stevec >= 5

    def getGameEnded(self, board, player):
        #print(self.display(board))
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.

        """
        # TODO optimizacija (preveri le presečišče z zadnjo potezo)

        # stolpci
        for stolpec in range(self.size):
            if self.pet_v_vrsto(self.DOL, player, (0, stolpec), board):
                return 1
            if self.pet_v_vrsto(self.DOL, -player, (0, stolpec), board):
                return -1

        # vrstice
        for vrstica in range(self.size):
            if self.pet_v_vrsto(self.DESNO, player, (vrstica, 0), board):
                return 1
            if self.pet_v_vrsto(self.DESNO, -player, (vrstica, 0), board):
                return -1

        # diagonale pod glavno diagonalo
        for vrstica in range(self.size):
            if self.pet_v_vrsto(self.DESNO_DOL, player, (vrstica, 0), board):
                return 1
            if self.pet_v_vrsto(self.DESNO_GOR, player, (vrstica, 0), board):
                return 1
            if self.pet_v_vrsto(self.DESNO_DOL, -player, (vrstica, 0), board):
                return -1
            if self.pet_v_vrsto(self.DESNO_GOR, -player, (vrstica, 0), board):
                return -1

        # diagonale nad glavno diagonalo
        for stolpec in range(1, self.size):
            if self.pet_v_vrsto(self.DESNO_DOL, player, (0, stolpec), board):
                return 1
            if self.pet_v_vrsto(self.DESNO_GOR, player, (0, stolpec), board):
                return 1
            if self.pet_v_vrsto(self.DESNO_DOL, -player, (0, stolpec), board):
                return -1
            if self.pet_v_vrsto(self.DESNO_GOR, -player, (0, stolpec), board):
                return -1
        

        # če smo tukaj, nihče ni zmagal
        for i, j in self.actions:
            if board[i][j] == 0:
                # we still in bejbiii
                return 0
        return 0.01

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        return player * board

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        # assert(len(pi) == self.n**2+1)  # 1 for pass
        pi_board = np.reshape(pi, (self.size, self.size))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()))]
        return l

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return str(board)

    @staticmethod
    def display(board):
        ans = ''
        for vrstica in board:
            for p in vrstica:
                if p == -1:
                    ans += " B "
                elif p == 1:
                    ans += " C "
                elif p == 0:
                    ans += " . "
                else:
                    raise TypeError("Ultra frkse stari.")
            ans += "\n"
        print(ans)
        return ans


class Gomoku():

    def odigraj_igro(self, igralec1=None, igralec2=None, logging=2, out=None):
        '''
        Odigra igro med vrsto igralca 1 in 2.
        TODO : verjetno je smiselno nardit objekt "možgani" namesto vrste igralca

        Parametri
        ---------
            igralec1, igralec2 (function) - funckija , ki sprejme stanje polja {-1,0,1}^225 in vrne action


        logging - integer (TODO a spremenimo?)

            0 - brez loginga
            1 - le zmage
            2 - igralna plošča vsak korak


        out (str) - 
            filename od datoteke za logging 
            (None za standardni output)

        Returns
        --------
        stanje igre na koncu (stanje.Stanje())
        '''
        vodja = Vodja(igralec1, igralec2)

        vodja.igramo_novo_igro(logging=logging, out=out)
        while True:
            stanje = vodja.igramo()
            if stanje is None:
                continue
            return stanje
