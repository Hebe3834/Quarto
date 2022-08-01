from quarto import *
import random


class Solver(Player):
    """
    A child of the Player class, randomly plays pieces
    """
    def __init__(self, name, is_p1):
        """Initialize the Solver"""
        self.score = 0
        self.name = name
        self.is_p1 = is_p1
        
    def pick(self, board, remaining_pieces, is_p1_turn):
        p = remaining_pieces[random.randrange(len(remaining_pieces))]
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " CHOSES " + str(p))
        return p

    def play_turn(self, board, piece, is_p1_turn):
        b = board.board
        empties = []
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] is None:
                    empties.append(str(j) + ',' + str(i)) # i and j swapped because user input x,y maps to y,x on the actual board
        p = random.choice(empties)
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " PLAYS " + p)
        return p