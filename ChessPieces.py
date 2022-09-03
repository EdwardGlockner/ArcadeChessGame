import pygame
import os
import time

pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)

# Loading special effect sounds
#check_sound = None
#game_over_sound = None

# Load piece sounds
pawn_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/pawn.wav"
bishop_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/bishop.wav"
knight_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/knight.mp3"
rook_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/rook.mp3"
queen_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/queen.mp3"
king_sound_path = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/king.mp3"


class Pieces():
    """ This is the parent class of all the chess pieces """
    def __init__(self, color, piece, position, image, sound_path):
        """
        @params:
            color: b for black, w for white
            piece: king/queen/rook/knight/bishop/pawn
            position: what position on the board
            image: image of the specific piece
        """
        self.color = color 
        self.piece = piece 
        self.position = position 
        self.image = image
        self.selected = False # Checks if the piece is selected or not 
        self.legal_moves_list = [] # All the legal moves to empty squares of the pieces
        self.killable_squares = [] # All the squares where the piece can kill another piece
        self.sound_path = sound_path

    def draw(self,win,position,color):
        """
        This method draws the chess piece. If the piece is selected all the
        potential moves is also drawn 
        @params:
            win: pygame window where the piece will be drawn
            position: position on the board
            color: color of the piece 
        @returns:
            void
        """

        drawThis = self.image

        if self.selected:
            if self.color == color:
                for move in self.legal_moves_list:
                    z = move[0]*100 + 50
                    w = move[1]*100 + 50
                    pygame.draw.circle(win, (255,0,0), (z,w), 10)

        x = position[0]*100 + 8
        y = position[1]*100 + 6.5

        win.blit(drawThis,(x,y))

    def on_board(self,pos):
        """
        This method checks if a position is on the board or not
        @params:
            pos: position on the board
        @returns:
            True if the position is on the board, False if it is not
        """

        if -1<pos[0]<8 and -1<pos[1]<8:
            return True
        else:
            return False

    def set_legal_moves(self, board):
        """
        This method updates all the possible moves of the piece
        @params:
            board: chess board created by the Board class
        @returns:
            void
        """

        self.legal_moves_list, self.killable_squares = self.legal_moves(board)

    def change_pos(self, pos):
        """
        This method change the position of the piece
        @params:
            pos: new position of the piece
        @returns:
            void
        """
   
        self.position[0]= pos[0]
        self.position[1] = pos[1]

# Now we create the children classes, of all the specific pieces

class Pawn(Pieces):
    def __init__(self, color, position, image):
        """
        @params:
            color: b for black, w for white
            position: what position on the board
            image: image of the specific piece
        """

        self.color = color
        self.position = position
        self.image = image
        # This keep tracks of when the pawn made the first double move (if it even did it), since then it can be taken through en passant
        self.first_double_move = 0 
        self.sound_path = pawn_sound_path

        Pieces.__init__(self, self.color, "pawn", self.position, self.image, self.sound_path)

    def legal_moves(self, board):
        """
        This method calculates all the legal moves
        @params:
            board: chess board created by the class Board
        @returns:
            moves: all legal moves to empty squares
            kill_squares: all squares where the piece can kill another piece
        """
        z = self.position[0]
        w = self.position[1]
        moves = []
        kill_squares = []

        if self.color == "w":
            if w == 6: # Allow two steps forward
                if board[z][w-1] == 0 and board[z][w-2] == 0: # so the squares are empty
                    moves.append((z,w-1))
                    moves.append((z,w-2))

            if board[z][w-1] == 0:
                moves.append((z,w-1))

            if z-1 > -1:
                if board[z-1][w-1] != 0:
                    if self.color != board[z-1][w-1].color: # check for opposite color
                        kill_squares.append((z-1,w-1))
            
            if z+1 < 8:
                if board[z+1][w-1] != 0:
                    if self.color != board[z+1][w-1].color:
                        kill_squares.append((z+1,w-1))
            
        else: # black
            if w == 1: # Allow two steps forward
                if board[z][w+1] == 0 and board[z][w+2] == 0:
                    moves.append((z,w+1))
                    moves.append((z,w+2))
            if self.on_board((z,w+1)):
                if board[z][w+1] == 0:
                    moves.append((z,w+1))

                if z+1 < 8:
                    if board[z+1][w+1] != 0:
                        if self.color != board[z+1][w+1].color:
                            kill_squares.append((z+1,w+1))
                if z-1 > -1:
                    if board[z-1][w+1] != 0:
                        if self.color != board[z-1][w+1].color:
                            kill_squares.append((z-1,w+1))

        return moves, kill_squares


class Rook(Pieces):
    def __init__(self, color, position, image):

        self.color = color
        self.position = position
        self.image = image
        self.sound_path = rook_sound_path
        self.moved = False # Check if the king has moved or not, so we can keep track of castling

        Pieces.__init__(self, self.color, "rook", self.position, self.image, self.sound_path)

    def legal_moves(self, board):

        z = self.position[0]
        w = self.position[1]

        moves = []
        kill_squares = []

        # checks a straight line for up, down right and left
        cross = [[[z + i, w] for i in range(1, 8 - z)],
             [[z - i, w] for i in range(1,z + 1)],
             [[z, w + i] for i in range(1, 8 - w)],
             [[z, w - i] for i in range(1, w + 1)]]

        for direction in cross:
            for positions in direction:
                if self.on_board(positions):
                    if board[positions[0]][positions[1]] != 0:
                        if self.color != board[positions[0]][positions[1]].color:
                            kill_squares.append((positions[0], positions[1]))
                        break
                    else:
                        moves.append((positions[0], positions[1]))


        return moves, kill_squares
 

class Queen(Pieces):
    def __init__(self, color, position, image):

        self.color = color
        self.position = position
        self.image = image
        self.sound_path = queen_sound_path

        Pieces.__init__(self, self.color, "queen", self.position, self.image, self.sound_path)

    def legal_moves(self, board):

        z = self.position[0]
        w = self.position[1]

        moves = []
        kill_squares = []

        # queen moves are the same as rook moves + bishop moves

        diagonals = [[[z + i, w + i] for i in range(1, 8)],
                 [[z + i, w - i] for i in range(1, 8)],
                 [[z - i, w + i] for i in range(1, 8)],
                 [[z - i, w - i] for i in range(1, 8)]]
        
        for direction in diagonals:
            for positions in direction:
                if self.on_board((positions[0],positions[1])):
                    if board[positions[0]][positions[1]] != 0:
                        if self.color != board[positions[0]][positions[1]].color:
                            kill_squares.append((positions[0], positions[1]))
                        break
                    else:
                        moves.append((positions[0],positions[1]))

        cross = [[[z + i, w] for i in range(1, 8 - z)],
             [[z - i, w] for i in range(1,z + 1)],
             [[z, w + i] for i in range(1, 8 - w)],
             [[z, w - i] for i in range(1, w + 1)]]

        for direction in cross:
            for positions in direction:
                if self.on_board(positions):
                    if board[positions[0]][positions[1]] != 0:
                        if self.color != board[positions[0]][positions[1]].color:
                            kill_squares.append((positions[0], positions[1]))
                        break
                    else:
                        moves.append((positions[0], positions[1]))

        return moves, kill_squares


class King(Pieces):
    def __init__(self, color, position, image):

        self.color = color
        self.position = position
        self.image = image
        self.sound_path = king_sound_path
        self.moved = False # Check if the king has moved or not, so we can keep track of castling

        Pieces.__init__(self, self.color, "king", self.position, self.image, self.sound_path)

    def legal_moves(self, board):

        z = self.position[0]
        w = self.position[1]

        moves = []
        kill_squares = []

        # checks a 3x3 square
        for y in range(3):
            for x in range(3):
                if self.on_board((z - 1 + y, w - 1 + x)):
                    if board[z - 1 + y][w - 1 + x] == 0:
                        moves.append((z-1+y, w-1+x))
                    else:
                        if self.color != board[z-1+y][w-1+x].color:
                            kill_squares.append((z-1+y, w-1+x))


        return moves, kill_squares


class Bishop(Pieces):
    def __init__(self, color, position, image):

        self.color = color
        self.position = position
        self.image = image
        self.sound_path = bishop_sound_path

        Pieces.__init__(self, self.color, "bishop", self.position, self.image, self.sound_path)

    def legal_moves(self, board):

        z = self.position[0]
        w = self.position[1]

        moves = []
        kill_squares = []

        # check the four diagonals
        diagonals = [[[z + i, w + i] for i in range(1, 8)],
                 [[z + i, w - i] for i in range(1, 8)],
                 [[z - i, w + i] for i in range(1, 8)],
                 [[z - i, w - i] for i in range(1, 8)]]
        

        for direction in diagonals:
            for positions in direction:
                if self.on_board((positions[0],positions[1])):
                    if board[positions[0]][positions[1]] != 0:
                        if self.color != board[positions[0]][positions[1]].color:
                            kill_squares.append((positions[0], positions[1]))
                        break
                    else:
                        moves.append((positions[0],positions[1]))

        return moves, kill_squares


class Knight(Pieces):
    def __init__(self, color, position, image):

        self.color = color
        self.position = position
        self.image = image
        self.sound_path = knight_sound_path

        Pieces.__init__(self, self.color, "knight", self.position, self.image, self.sound_path)

    def legal_moves(self, board):

        z = self.position[0]
        w = self.position[1]

        moves = []
        kill_squares = []

        # checks a 5x5 square
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i**2 + j**2  == 5: # pythagorean theorem
                    if self.on_board((z+i,w+j)):
                        if board[z+i][w+j] == 0:
                            moves.append((z+i,w+j))
                        else:
                            if self.color != board[z+i][w+j].color:
                                kill_squares.append((z+i, w+j))

        return moves, kill_squares
