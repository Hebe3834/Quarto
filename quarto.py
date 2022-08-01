#!/usr/bin/env python3

# random
# win if possible (play)
# don't give piece that loses (pick)

from termcolor import colored
from solver import *

class Quarto():
    """
    Manages the game state
    """
    def __init__(self):
        """Creates an empty 4x4 Quarto board"""
        self.remaining_pieces = []
        self.board = []
        self.reset_board()


    def reset_board(self):
        self.remaining_pieces = [Piece(a, b, c, d) for a in [True, False] for b in [True, False] for c in [True, False] for d in [True, False]]
        self.board =  [[None for i in range(4)] for j in range(4)]


    def row(self, r):
        '''Returns one row of the board, formatted for printing'''
        return " " + " | ".join([("   " if t is None else str(t)) \
                                for t in self.board[r]]) + " "

    def play(self, piece, coord):
        '''
        Attempts to place token in the position (coord[0], coord[1])
        If it is a valid move updates the board
        Checks if the current player has won the game
        '''
        if not (len(coord) == 2 and coord[0].isdigit() and coord[1].isdigit()):
            print("PLEASE ENTER TWO INTEGERS IN THE FORMAT X,Y")
            return False
        x = int(coord[0])
        y = int(coord[1])
        if not (0 <= x < 4 and 0 <= y < 4 and len(coord) == 2):
            print("COORDINATES MUST BE A LIST OF TWO INTS FROM 0 TO 3 INCLUSIVE. PLEASE TRY AGAIN.")
        elif not self.board[y][x] is None:
            print("THIS BOX IS ALREADY TAKEN WITH " + str(self.board[y][x]) + "PLEASE TRY AGAIN")
        else:
            self.board[y][x] = piece
            # print(self)
            return True
        return False


    def checkList(self, gen):
        '''
        Checks if the list generator contains one of the same characteristic
        '''
        lst = list(gen)
        key = lst[0]
        win = True
        for i in lst:
            if i is None or i.size != key.size:
                win = False
                break
        if win: return True
        win = True
        for i in lst:
            if i is None or i.color != key.color:
                win = False
                break
        if win: return True
        win = True
        for i in lst:
            if i is None or i.shape != key.shape:
                win = False
                break
        if win: return True
        win = True
        for i in lst:
            if i is None or i.hollow != key.hollow:
                win = False
                break
        if win: return True
        return False

    def checkWin(self, coord):
        '''
        Checks if the player has won by looking at elements vertically, horizontally, and diagonally
        '''
        x = int(coord[0])
        y = int(coord[1])
        if self.checkList(self.board[y][c] for c in range(4)): #row
            return True
        if self.checkList(self.board[r][x] for r in range(4)): #col
            return True
        if x == y and self.checkList(self.board[j][j] for j in range(4)): # diagonal \
            return True
        if y == 4-x-1 and self.checkList(self.board[j][4 - j - 1] for j in range(4)): # diagonal /
            return True
        return False

    def isBoardFull(self):
        '''Checks if there are any spots left on the Board to fill'''
        for i in self.board:
            for j in i:
                if j is None:
                    return False
        return True

    def __str__(self):
        '''Returns the formatted board'''
        hline = "\n# >---------------------< #\n"
        rows = []
        for i in range(4):
            rows.append("# " + self.row(i) + " #")
        output = "\nX^*^*^*^*^*^*^*^*^*^*^*^*^X\n"
        output += hline.join(rows)
        output += "\nX^*^*^*^*^*^*^*^*^*^*^*^*^X"
        return output

    def __repr__(self):
        '''Returns the board as a list'''
        return str(self.board)






class Piece():
    """
    Represents one piece to be placed on the Quarto board
    """
    def __init__(self, size, color, shape, hollow):
        """
        Creates the game Piece and sets up its attributes
            `size` is True if Piece is tall
            `color` is True if Piece is light brown
            `shape` is True if Piece is rectangular
            `hollow` is True if Piece is hollow
        """
        self.size = size
        self.color = color
        self.shape = shape
        self.hollow = hollow

    def __str__(self):
        '''Returns the piece as an ascii representation'''
        pic = "[]" if self.shape else "()"
        pic = pic[0] + ("#" if self.hollow else " ") + pic[1]
        pic1 = colored(pic, ("cyan" if self.color else "magenta"), attrs=[("underline" if self.size else "bold")])
        return pic1
        # return ("t" if self.size else "s") + \
        #         ("l" if self.color else "d") + \
        #         ("r" if self.shape else "c") + \
        #         ("h" if self.hollow else "f")
        
    def __repr__(self):
        '''Returns the piece as a string of characters'''
        return ("t" if self.size else "s") + \
                ("l" if self.color else "d") + \
                ("r" if self.shape else "c") + \
                ("h" if self.hollow else "f")
        
        
        # """Returns information about the Piece's attributes"""
        # return "Piece is " + ("tall" if self.size else "short") + ", " \
        #                 + ("light" if self.color else "dark") + ", " \
        #                 + ("rectangular" if self.shape else "circular") + ", " \
        #                 + "and " + ("hollow" if self.hollow else "filled") 



class Player():
    """
    Represents a Quarto player
    """
    def __init__(self, name):
        """Initialize the player"""
        self.score = 0
        self.name = name

    def pick(self, board, remaining_pieces, is_p1_turn):
        print(board)
        print("Pieces left: " + "  ".join((str(i) + ":" + str(t)) \
                                        for i,t in enumerate(remaining_pieces)))
        nextPiece_ind = (input("\n" + colored(self.name, ("red" if is_p1_turn else "green")) + \
                            ": Please select a piece to give your opponent (index from list above): "))
        while not (nextPiece_ind.isdigit()) or not (0 <= int(nextPiece_ind) < len(remaining_pieces)):
            print("\nINDICES MUST BE AN INTEGER FROM 0 TO " + str(len(remaining_pieces) - 1) + ". TRY AGAIN")
            nextPiece_ind = (input("\n" + colored(self.name, ("red" if is_p1_turn else "green")) + \
                            ": Please select a piece to give your opponent (index from list above): "))
        return remaining_pieces[int(nextPiece_ind)]

    def play_turn(self, board, piece, is_p1_turn):
        '''Gathers player decision on where to play piece'''
        print(board)
        return input("\n" + colored(self.name, ("red" if is_p1_turn else "green")) + " is up with Piece " + str(piece) + ". Please enter coordinates x,y: ")


    def __str__(self):
        '''Prints info about the player's name and score'''
        return "Player " + str(self.name) + " with " + str(self.score) + " point(s)."







class GameManager():
    """
    The GameManager runs the main control loop of the Quarto game
    To play, create a new GameManager 'game' then run 'game.play_game()'
    """

    def __init__(self, player1_name, player2_name):
        """
        Starts the game with a board, two players
        If a player's name starts with 'Solver' (ie 'Solver_Billy'), that player is replaced with a cpu
        """
        if player1_name[:6] == "Solver":
            self.player1 = Solver(player1_name, True)
        else:
            self.player1 = Player(player1_name)
        if player2_name[:6] == "Solver":
            self.player2 = Solver(player2_name, False)
        else:
            self.player2 = Player(player2_name)        
        self.quarto = Quarto()
        self.p1_turn = True

    def play_game(self):
        '''
        Allows two players to play the current tic-tac-toe game.
        Continuously asks for the current player's input
        Ends when either a player has won or the board is full
        '''
        print("Pieces left: " + "  ".join((str(i) + ":" + str(t)) \
                                        for i,t in enumerate(self.quarto.remaining_pieces)))
        nextPiece = self.player1.pick(self.quarto, self.quarto.remaining_pieces, True) # player1 picks a piece to give payer2
        self.p1_turn = False

        while True:
            if not self.p1_turn:    # Starts with player 2 because player one pics the first piece 
                # print(self.quarto)
                coords = self.player2.play_turn(self.quarto, nextPiece, False)
                print("\n============================================================")
                while not self.quarto.play(nextPiece, coords.split(",")): # same player attempts to give a valid move until successful
                    coords = self.player2.play_turn(self.quarto, nextPiece, False)
                self.p1_turn = True # switch to player 1 turn
                self.quarto.remaining_pieces.remove(nextPiece)
                if self.quarto.checkWin(coords.split(",")):
                    print("Congratulations! " + colored(self.player2.name, "green") + " has won the game.")
                    self.player2.score += 1
                    print(self)
                    break
                if len(self.quarto.remaining_pieces) == 0: # No pieces left; tie
                    print("Game Over! Tie")
                    
                    print(self)
                    self.reset_board() # reset board for new game; losing player goes first next round
                    break
                nextPiece = self.player2.pick(self.quarto, self.quarto.remaining_pieces, False)
            else:
                # print(self.quarto)
                coords = self.player1.play_turn(self.quarto, nextPiece, True)
                print("\n============================================================")
                while not self.quarto.play(nextPiece, coords.split(",")): # same player attempts to give a valid move until successful
                    coords = self.player1.play_turn(self.quarto, nextPiece, False)
                self.p1_turn = False # switch to player 2 turn
                self.quarto.remaining_pieces.remove(nextPiece)
                if self.quarto.checkWin(coords.split(",")):
                    print("Congratulations! " + colored(self.player1.name, "red") + " has won the game.")
                    self.player1.score += 1
                    print(self)
                    break
                if len(self.quarto.remaining_pieces) == 0: # no pieces left; tie
                    print("Game Over! Tie")
                    print(self)
                    self.reset_board() # reset board for new game; losing player goes first next round
                    break
                nextPiece = self.player1.pick(self.quarto, self.quarto.remaining_pieces, True)
            # if self.quarto.isBoardFull() or len(self.quarto.remaining_pieces) == 0:
            #     print(self.quarto)
            #     print("Game Over! Tie")
            #     self.reset_board() # reset board for new game; losing player goes first next round
            #     break

    def reset_board(self):
        '''Changes the board to an empty board'''
        self.quarto.reset_board()

    def __str__(self):
        '''Prints all the info about the game, including the current board and info on each player'''
        return str(self.quarto) + "\n\n" + colored(str(self.player1), 'red') + "\n" + colored(str(self.player2), 'green')







def main():
    '''
    Main function: sets up the game
                   displays rules and prompts
                   allows for new game after one has finished
    '''

    print(colored("\n\n\n\n\nWelcome to Quarto!", 'grey', attrs=["bold"]))
    print(colored("Fill up an entire row, column, or diagonal with a matching attribute to win.", 'grey'))
    
    print(colored('\nAttributes:', 'grey', attrs=["underline"]))
    print(" - " + colored("Underline", 'grey', attrs=["underline"]) + colored(" or ", 'grey') + colored("Bold", 'grey', attrs=["bold"]))    
    print(" - " + colored("Cyan", 'cyan') + colored(" or ", 'grey') + colored("Magenta", 'magenta'))
    print(colored(" - [Square] or (Round)", 'grey'))
    print(colored(" - Filled [#] (#)   or   Hollow [ ] ( )", 'grey'))

    print(colored('\ny equals row (distance from top row)\nx equals column (distance from leftmost row)\n\n', 'grey'))
    p1_name = input(colored("Name of Player 1: ", "red"))
    p2_name = input(colored("Name of Player 2: ", "green"))

    game = GameManager(p1_name, p2_name)

    while True:
        game.reset_board()
        print("\n\nNow Playing: Quarto with " + colored(p1_name, "red") + " and " + colored(p2_name, "green") + "\n")
        game.play_game()
        response = input("\nPlay again? (Y/N) ")
        if response == "N" or response == "n":
            print("Thank you for playing :)\n")
            break
        # Any other response continues to a new game



if __name__ == "__main__": main()






# COLORS:
# grey
# red
# green
# yellow
# blue
# magenta
# cyan
# white

# HIGHLIGHTS: 
# on_grey
# on_red
# on_green
# on_yellow
# on_blue
# on_magenta
# on_cyan
# on_white





#  [#] [ ] (#) ( )  
