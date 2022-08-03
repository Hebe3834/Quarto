from quarto import *
import random


class RandSolver(Player):
    """
    A child of the Player class
    Randomly plays and selects pieces
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

    def play_turn(self, quarto, piece, is_p1_turn):
        b = quarto.board
        empties = []
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] is None:
                    empties.append(str(j) + ',' + str(i)) # i and j swapped because user input x,y maps to y,x on the actual board
        p = random.choice(empties)
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " PLAYS " + p)
        return p





class WinSolver(Player):
    """
    A child of the Player class
    Places Piece in a winning spot if possible during the current turn
        else places Piece in a random spot
    Picks random Pieces
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

    def play_turn(self, quarto, piece, is_p1_turn):
        b = quarto.board
        test_board = quarto.clone()
        test_piece = piece.clone()
        empties = []
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] is None:     # if spot is empty, try playing it in a copy of the current board
                    if test_board.board[i][j] is None:      # play test_piece if spot on test_board is empty
                        test_board.board[i][j] = test_piece
                        # print(str(j) + ", " + str(i))
                        if test_board.checkWin([str(j),str(i)]):
                            return str(j) + ',' + str(i)
                        test_board.board[j][i] = None           # reaching here means winning piece not found; reset test_board
                        empties.append(str(j) + ',' + str(i)) # i and j swapped because user input x,y maps to y,x on the actual board
        p = random.choice(empties)
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " PLAYS " + p)
        return p





class LosentSolver(Player):
    """
    A child of the Player class
    Places Piece in a winning spot if possible during the current turn
        else places Piece in a random spot
    Picks random Pieces that would not allow the opponent to win in the next turn
    """
    def __init__(self, name, is_p1):
        """Initialize the Solver"""
        self.score = 0
        self.name = name
        self.is_p1 = is_p1
        
    def pick(self, quarto, remaining_pieces, is_p1_turn):
        b = quarto.board
        safe_pieces = []
        for p in remaining_pieces:
            test_piece = p.clone()
            test_board = quarto.clone()
            is_piece_safe = True
            for i in range(len(b)):         # try putting the piece into all spots on board
                for j in range(len(b[i])):
                    if b[i][j] is None:     # if spot is empty, try playing it in a copy of the current board
                        test_board.board[i][j] = test_piece
                        if test_board.checkWin([str(j),str(i)]):
                            is_piece_safe = False
                        test_board.board[i][j] = None
            if is_piece_safe:
                safe_pieces.append(p)
            is_piece_safe = True
        if len(safe_pieces) == 0:       # no safe pieces; accept defeat and play a random piece
            p = remaining_pieces[random.randrange(len(remaining_pieces))]
        else:
            p = safe_pieces[random.randrange(len(safe_pieces))]
        # print(safe_pieces)
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " CHOSES " + str(p))
        return p

    def play_turn(self, quarto, piece, is_p1_turn):
        b = quarto.board
        test_board = quarto.clone()
        test_piece = piece.clone()
        empties = []
        for i in range(len(b)):
            for j in range(len(b[i])):
                if b[i][j] is None:     # if spot is empty, try playing it in a copy of the current board
                    if test_board.board[i][j] is None:      # play test_piece if spot on test_board is empty
                        test_board.board[i][j] = test_piece
                        # print(str(j) + ", " + str(i))
                        if test_board.checkWin([str(j),str(i)]):
                            return str(j) + ',' + str(i)
                        test_board.board[j][i] = None           # reaching here means winning piece not found; reset test_board
                        empties.append(str(j) + ',' + str(i)) # i and j swapped because user input x,y maps to y,x on the actual board
        p = random.choice(empties)
        print("\n" + colored(self.name, ('red' if self.is_p1 else 'green')) + " PLAYS " + p)
        return p