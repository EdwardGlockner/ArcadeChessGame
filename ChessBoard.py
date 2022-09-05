
import time
import sys


import pygame
import os
 
from ChessPieces import Pawn
from ChessPieces import Bishop
from ChessPieces import Rook
from ChessPieces import Knight
from ChessPieces import Queen
from ChessPieces import King
from ChessPieces import Pieces

import copy



font_name = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/fonts/PressStart2P-Regular.ttf"
WIDTH = 800
HEIGHT = 800
pro_size = (708,708)

# Load and initiate all the sounds
pygame.mixer.init()
pygame.mixer.music.set_volume(0.05)
promote = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/promote.wav")
promote.set_volume(0.15)
after_promotion = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/after_promotion.wav")
kill_sound = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/kill_sound.wav")
check_sound = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/check_sound.mp3")
check_sound.set_volume(0.8)
castle_sound = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/castle.wav")
castle_sound.set_volume(0.05)

# Load all the images
piece_size = (92,92)
b_bishop = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_bishop.png")), piece_size)
b_rook = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_rook.png")), piece_size)
b_pawn = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_pawn.png")), piece_size)
b_knight = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_knight.png")), piece_size)
b_king = pygame.transform.scale(pygame.image.load(os.path.join("img", "//Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_king.png")), piece_size)
b_queen = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/b_queen.png")), piece_size)

#b_bishop = pygame.transform.rotate(b_bishop, 180)
#b_rook = pygame.transform.rotate(b_rook, 180)
#b_pawn = pygame.transform.rotate(b_pawn, 180)
#b_knight = pygame.transform.rotate(b_knight, 180)
#b_king = pygame.transform.rotate(b_king, 180)
#b_queen = pygame.transform.rotate(b_queen, 180)

w_bishop = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_bishop.png")), piece_size)
w_rook = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_rook.png")), piece_size)
w_pawn = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_pawn.png")), piece_size)
w_knight = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_knight.png")), piece_size)
w_king = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_king.png")), piece_size)
w_queen = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/w_queen.png")), piece_size)

class Board():
    """ This class handles the chess board and different events such as when a piece
    is selected, check or checkmate, or deselecting pieces """
    def __init__(self,rows,cols):
        """
        @params:
            rows: rows of the chess board
            cols: collumns of the chess board
        """
        self.rows = rows
        self.cols = cols

        self.board = [[0 for x in range(self.cols)] for _ in range(self.rows)]

        # Create the starting position
        self.board[0][0] = Rook("b", [0,0], b_rook)
        self.board[1][0] = Knight("b", [1,0], b_knight)
        self.board[2][0] = Bishop("b", [2,0], b_bishop)
        self.board[3][0] = Queen("b", [3,0], b_queen)
        self.board[4][0] = King("b", [4,0], b_king)
        self.board[5][0] = Bishop("b", [5,0], b_bishop)
        self.board[6][0] = Knight("b", [6,0], b_knight)
        self.board[7][0] = Rook("b", [7,0], b_rook)

        self.board[0][1] = Pawn("b", [0,1], b_pawn)
        self.board[1][1] = Pawn("b", [1,1], b_pawn)
        self.board[2][1] = Pawn("b", [2,1], b_pawn)
        self.board[3][1] = Pawn("b", [3,1], b_pawn)
        self.board[4][1] = Pawn("b", [4,1], b_pawn)
        self.board[5][1] = Pawn("b", [5,1], b_pawn)
        self.board[6][1] = Pawn("b", [6,1], b_pawn)
        self.board[7][1] = Pawn("b", [7,1], b_pawn)

        self.board[0][6] = Pawn("w", [0,6], w_pawn)
        self.board[1][6] = Pawn("w", [1,6], w_pawn)
        self.board[2][6] = Pawn("w", [2,6], w_pawn)
        self.board[3][6] = Pawn("w", [3,6], w_pawn)
        self.board[4][6] = Pawn("w", [4,6], w_pawn)
        self.board[5][6] = Pawn("w", [5,6], w_pawn)
        self.board[6][6] = Pawn("w", [6,6], w_pawn)
        self.board[7][6] = Pawn("w", [7,6], w_pawn)

        self.board[0][7] = Rook("w", [0,7], w_rook)
        self.board[1][7] = Knight("w", [1,7], w_knight)
        self.board[2][7] = Bishop("w", [2,7], w_bishop)
        self.board[3][7] = Queen("w", [3,7], w_queen)
        self.board[4][7] = King("w", [4,7], w_king)
        self.board[5][7] = Bishop("w", [5,7], w_bishop)
        self.board[6][7] = Knight("w", [6,7], w_knight)
        self.board[7][7] = Rook("w", [7,7], w_rook)

        self.team_order = ["w", "b"]
        self.turn = "w" # To keep track whose turn it is
        self.number_of_moves = 0
        self.checkmate = ""

    def draw_board(self,win):
        """
        This method draws the entire board, by iterating over all pieces, and drawing them
        individually
        @params:
            win: pygame window where the board will be drawn
        @returns:
            void
        """

        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    pos = [i,j]
                    self.board[i][j].draw(win, pos, self.turn)

    def select_piece(self, pos):
        """
        This method keeps track of selecting pieces, and moving them
        @param:
            pos: position where the user clicked on the board
        @returns:
            void
        """
        # we get the previous position of the piece, by finding which piece is selected
        prev = (-1,-1)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i,j)
    

        self.update_legal_moves() # update all the moves
        
        if self.board[prev[0]][prev[1]] != 0: moves = self.board[prev[0]][prev[1]].legal_moves_list
        else: moves = []
        print(moves)
        # if the new position is empty, move it there if it is in legal moves
        if self.board[pos[0]][pos[1]] == 0:
            if (pos[0], pos[1]) in moves:
                if self.turn == self.board[prev[0]][prev[1]].color:
                    if self.board[prev[0]][prev[1]].piece == "rook" or self.board[prev[0]][prev[1]].piece == "king":
                        self.board[prev[0]][prev[1]].moved = True
                    
                    self.move(prev,pos)
                    self.deselect_piece()
                    self.number_of_moves += 1
                    self.turn = self.team_order[self.number_of_moves % len(self.team_order)]

                    if self.board[pos[0]][pos[1]].piece == "pawn": # Checks if it was a double move
                        if abs(prev[1]-pos[1]) == 2:
                            self.board[pos[0]][pos[1]].first_double_move = self.number_of_moves

                    if self.check(self.turn, self.board):
                        check_sound.play()
                    else:
                        pygame.mixer.Sound(self.board[pos[0]][pos[1]].sound_path).play()

                    

        else: # if it is not in legal moves, deselect all the pieces
            self.deselect_piece()
            self.board[pos[0]][pos[1]].selected = True

        # if the new position is not empty, we kill the piece if it is in killable moves
        if self.board[pos[0]][pos[1]] != 0: 
            if self.board[prev[0]][prev[1]] != 0:
                killable_squares = self.board[prev[0]][prev[1]].killable_squares
                if (pos[0], pos[1]) in killable_squares:
                    if self.turn == self.board[prev[0]][prev[1]].color:
                        self.board[pos[0]][pos[1]] == 0
                        if self.board[prev[0]][prev[1]].piece == "rook" or self.board[prev[0]][prev[1]].piece == "king":
                            self.board[prev[0]][prev[1]].moved = True

                        self.move(prev,pos)
                        self.deselect_piece()
                        self.number_of_moves += 1
                        self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                        kill_sound.play()

        # check for en passant
        """
        if self.board[prev[0]][prev[1]] != 0:
            if self.board[prev[0]][prev[1]].piece == "pawn":
                if self.board[prev[0]][prev[1]].color == "w":
                    try:
                        if self.board[pos[0]][pos[1]+1] != 0:
                            if self.board[pos[0]][pos[1]+1].piece == "pawn":
                                if self.board[pos[0]][pos[1]+1].color == "b":
                                    if self.board[pos[0]][pos[1]+1].first_double_move == self.number_of_moves:
                                        self.move(prev, (pos[0], pos[1]+1))
                                        self.move((pos[0], pos[1]+1),pos)
                                        self.number_of_moves +=1
                                        self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                    except Exception: # Outside board
                        pass

                else:
                    try:
                        if self.board[pos[0]][pos[1]-1] != 0:
                            if self.board[pos[0]][pos[1]-1].piece == "pawn":
                                if self.board[pos[0]][pos[1]-1].color == "w":
                                    if self.board[pos[0]][pos[1]-1].first_double_move == self.number_of_moves:
                                        self.move(prev, (pos[0], pos[1]-1))
                                        self.move((pos[0], pos[1]-1),pos)
                                        self.number_of_moves += 1
                                        self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                    except Exception: # Outside board
                        pass
        """
        if abs(prev[1]-pos[1]) == 1:
            if self.board[prev[0]][prev[1]] != 0 and self.board[prev[0]][prev[1]].piece == "pawn":
                if self.board[pos[0]][pos[1]] == 0:
                    if self.board[prev[0]][prev[1]].color == "w":
                        try:
                            if self.board[pos[0]][pos[1]+1] != 0 and self.board[pos[0]][pos[1]+1].piece == "pawn":
                                    if self.board[pos[0]][pos[1]+1].color == "b":
                                        if self.board[pos[0]][pos[1]+1].first_double_move == self.number_of_moves:
                                            self.move(prev, (pos[0], pos[1]+1))
                                            self.move((pos[0], pos[1]+1), pos)
                                            self.number_of_moves += 1
                                            self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                                            pygame.mixer.Sound(self.board[pos[0]][pos[1]].sound_path).play()
                        except Exception:
                            pass


                    else: # black color
                        try:
                            if self.board[pos[0]][pos[1]-1] != 0 and self.board[pos[0]][pos[1]-1].piece == "pawn":
                                if self.board[pos[0]][pos[1]-1].color == "w":
                                    if self.board[pos[0]][pos[1]-1].first_double_move == self.number_of_moves:
                                        self.move(prev, (pos[0], pos[1]-1))
                                        self.move((pos[0], pos[1]-1), pos)
                                        self.number_of_moves += 1
                                        self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                                        pygame.mixer.Sound(self.board[pos[0]][pos[1]].sound_path).play()
                        except Exception:
                            pass

        
        # check if the player wants to castle
        if self.board[prev[0]][prev[1]] and self.board[pos[0]][pos[1]] != 0:
            if self.board[prev[0]][prev[1]].piece == "king" and self.board[prev[0]][prev[1]].moved == False:
                if self.board[pos[0]][pos[1]].piece == "rook" and self.board[pos[0]][pos[1]].moved == False:
                    if self.board[prev[0]][prev[1]].color == self.board[pos[0]][pos[1]].color: # so they are the same color
                        delta_x = pos[0] - prev[0]
                        if delta_x > 0:
                            new_rook_pos = (prev[0]+1, prev[1])
                            new_king_pos = (new_rook_pos[0]+1, new_rook_pos[1])

                            controll = True

                            for i in range(1,new_king_pos[0] - prev[0]+1):
                                if not self.board[prev[0] + i][prev[1]] == 0:
                                    controll = False
                                if self.temp_board(prev, (prev[0]+i, prev[1])):
                                    controll = False

                            if controll:
                                self.move(prev, new_king_pos)
                                self.move(pos, new_rook_pos)
                                self.number_of_moves += 1
                                self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                                self.board[new_rook_pos[0]][new_rook_pos[1]].moved = True
                                self.board[new_king_pos[0]][new_king_pos[1]].moved = True
                                castle_sound.play()


                        if delta_x < 0:
                            new_rook_pos = (prev[0]-1, prev[1])
                            new_king_pos = (new_rook_pos[0]-1, new_rook_pos[1])

                            controll = True

                            for i in range(1, prev[0]+1 - new_king_pos[0]):
                                if not self.board[prev[0] - i][prev[1]] == 0:
                                    controll = False
                                if self.temp_board(prev, (prev[0]-i, prev[1])):
                                    controll = False

                            if controll:
                                self.move(prev, new_king_pos)
                                self.move(pos, new_rook_pos)
                                self.number_of_moves +=1
                                self.turn = self.team_order[self.number_of_moves % len(self.team_order)]
                                self.board[new_rook_pos[0]][new_rook_pos[1]].moved = True
                                self.board[new_king_pos[0]][new_king_pos[1]].moved = True
                                castle_sound.play()

    def deselect_piece(self):
        """
        This method deselects all the pieces
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def update_legal_moves(self):
        """
        This method updates all the legal moves (both killable and not), and also checks for checkmate
        """
        all_moves = []
        for i in range(self.cols):
            for j in range(self.cols):
                if type(self.board[i][j]) != int: # so the square is not empty
                    if self.board[i][j].color == self.turn:  # so its the right player who moves the pieces
                        self.board[i][j].set_legal_moves(self.board) # get all the moves
                    
                        legalmoves1 = self.board[i][j].legal_moves_list
                        killermoves1 = self.board[i][j].killable_squares
                        # checks so a move doesnt put the player into check
                        
                        self.board[i][j].killable_squares = [move for move in killermoves1 if not self.temp_board((i,j), move)]
                        self.board[i][j].legal_moves_list = [move for move in legalmoves1 if not self.temp_board((i,j),move)]
                    
                        all_moves.append(self.board[i][j].killable_squares)
                        all_moves.append(self.board[i][j].legal_moves_list)

        all_moves = list(filter(None, all_moves)) # remove empty lists

        if len(all_moves) == 0: # Checkmate if there is no legal moves
            self.checkmate = self.turn

    def temp_board(self, start, end):
        """
        This method creates a copy of the chess board without reference to it, 
        so we can see if a chess move moves a player into check or not
        @params:
            start: start position of the piece
            end: end position of the piece
        @returns:
            return True if the piece doesnt move the player into check
        """
        """
        
        tempo_board = self.copy_board() # copy of the board without reference
        tempo_board[start[0]][start[1]].change_pos((end[0],end[1]))
        tempo_board[end[0]][end[1]] = tempo_board[start[0]][start[1]]
        tempo_board[start[0]][start[1]] = 0
        if self.check(self.turn,tempo_board): # check if it moves to player into check or not
            return True
        else:
            return False
        
        """
        nBoard = self.copy()


        if nBoard[start[0]][start[1]] != 0:
            new = nBoard[end[0]][end[1]]

            nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
            nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
            nBoard[start[0]][start[1]] = 0

            if self.check(self.turn, nBoard):

                return True


        return False


    def copy(self):
        copyobj = Board(8, 8)
        #
        for i in range(self.cols):
            for j in range(self.rows):
                if self.board[j][i] != 0:
                    for name, attr in self.board[j][i].__dict__.items():
                        if self.board[j][i].piece == "rook":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = Rook("b", [j,i], b_rook)
                            else:
                                copyobj.board[j][i] = Rook("w", [j,i], w_pawn)

                        elif self.board[j][i].piece == "knight":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = Knight("b", [j,i], b_knight)
                            else:
                                copyobj.board[j][i] = Knight("w", [j,i], w_knight)

                        elif self.board[j][i].piece == "bishop":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = Bishop("b", [j,i], b_bishop)
                            else:
                                copyobj.board[j][i] = Bishop("w", [j,i], w_bishop)

                        elif self.board[j][i].piece == "queen":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = Queen("b", [j,i], b_queen)
                            else:
                                copyobj.board[j][i] = Queen("w", [j,i], w_queen)

                        elif self.board[j][i].piece == "king":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = King("b", [j,i], b_king)
                            else:
                                copyobj.board[j][i] = King("w", [j,i], w_king)

                        elif self.board[j][i].piece == "pawn":
                            if self.board[j][i].color == "b":
                                copyobj.board[j][i] = Pawn("b", [j,i], b_pawn)
                            else:
                                copyobj.board[j][i] = Pawn("w", [j,i], w_pawn)

                        try:
                            copyobj.board[j][i].__dict__[name] == copy.deepcopy(attr)
                            #print("deep: ", "name: ", name, "attr: ", attr)



                        except:
                            copyobj.board[j][i].__dict__[name] = copy.copy(attr)
                            #print("shallow: ", "name: ", name, " attr: ", attr)
                            

        return copyobj.board

    def move(self, start, end):
        """
        This method moves a piece
        @params:
            start: start position of the piece
            end: end position of the piece
        """
        nBoard = self.board[:]
        nBoard[start[0]][start[1]].change_pos((end[0],end[1]))
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        nBoard[start[0]][start[1]] = 0
        self.board = nBoard

    def check(self, color, board):
        """ 
        Checks if the king is in check or not
        @params:
            color: color of the king
            board: board to be analyzed
        @returns:
            True if the king is in check, False otherwise
        """
        king_pos = (-1,-1)
        killer_moves = []
        for i in range(self.cols):
            for j in range(self.rows):
                if board[i][j] != 0:
                    if board[i][j].piece == "king":
                        if board[i][j].color == color:
                            king_pos = (i,j)

                    board[i][j].set_legal_moves(board)
                    if board[i][j].color != color:
                        killer_moves.append(board[i][j].killable_squares)

        check = False
        for killer_move in killer_moves:
            if king_pos in killer_move:
                check = True
                break

        return check

    def promote(self,win):


        rect_size = (0.1*WIDTH, 0.1*WIDTH ,0.8*WIDTH, 0.2*WIDTH) # [left, top, width, height]
        arcade_bg = pygame.transform.scale(pygame.image.load(os.path.join('img', '/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/images/arcade_bg.jpg')), (rect_size[2],rect_size[3]))

        for i in range(self.rows):
                if self.board[i][0] != 0:
                    if self.board[i][0].piece == "pawn": # white pawn needs to promote
                        pygame.font.init()
                        font = pygame.font.Font(font_name,30)
                        txt = font.render("PROMOTE PAWN",1,(255,95,133))
                        controll = True
                        while controll:
                            promote.play(-1)
                            win.blit(txt, (WIDTH/2 - txt.get_width()/2, 25))
                            
                            win.blit(arcade_bg, rect_size)
                            
                            win.blit(w_bishop, (0.1*WIDTH +40, 0.15*WIDTH))
                            win.blit(w_knight, (0.1*WIDTH + 0.2*WIDTH + 40, 0.15*WIDTH))
                            win.blit(w_rook, (0.1*WIDTH + 0.4*WIDTH +40, 0.15*WIDTH))
                            win.blit(w_queen, (0.1*WIDTH + 0.6*WIDTH +40, 0.15*WIDTH))
                            pygame.display.update()
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    if 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH +40 + pro_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + pro_size[1]: #Bishop
                                        self.board[i][0] == 0
                                        self.board[i][0] = Bishop("w", [i,0], w_bishop)
                                        promote.stop()
                                        controll = False
                                        
                                    elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.2*WIDTH +40 + pro_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + pro_size[1]: # Knight
                                        self.board[i][0] == 0
                                        self.board[i][0] = Knight("w", [i,0], w_knight)
                                        promote.stop()
                                        controll = False
                                        break
                                    elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.4*WIDTH +40 + pro_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + pro_size[1]: # Rook
                                        self.board[i][0] == 0
                                        self.board[i][0] = Rook("w", [i,0], w_rook)
                                        promote.stop()
                                        controll = False
                                        break
                                    elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.6*WIDTH +40 + pro_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + pro_size[1]: # Queen
                                        self.board[i][0] == 0
                                        self.board[i][0] = Queen("w", [i,0], w_queen)
                                        promote.stop()
                                        controll = False
                                        break
                        after_promotion.play()
                            

        for i in range(self.rows):
            if self.board[i][7] != 0:
                if self.board[i][7].piece == "pawn": # white pawn needs to promote
                    pygame.font.init()
                    font = pygame.font.Font(font_name,30)
                    txt = font.render("PROMOTE PAWN",1,(255,95,133))
                    controll = True
                    while controll:
                        promote.play(-1)
                        win.blit(txt, (WIDTH/2 - txt.get_width()/2, 25))

                        win.blit(arcade_bg, rect_size)
                        
                        win.blit(b_bishop, (0.1*WIDTH +40, 0.15*WIDTH))
                        win.blit(b_knight, (0.1*WIDTH + 0.2*WIDTH + 40, 0.15*WIDTH))
                        win.blit(b_rook, (0.1*WIDTH + 0.4*WIDTH +40, 0.15*WIDTH))
                        win.blit(b_queen, (0.1*WIDTH + 0.6*WIDTH +40, 0.15*WIDTH))
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                pos = pygame.mouse.get_pos()
                                if 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH +40 + piece_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + piece_size[1]: #Bishop
                                    self.board[i][7] == 0
                                    self.board[i][7] = Bishop("b", [i,7], b_bishop)
                                    promote.stop()
                                    controll = False
                                    
                                elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.2*WIDTH +40 + piece_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + piece_size[1]: # Knight
                                    self.board[i][7] == 0
                                    self.board[i][7] = Knight("b", [i,7], b_knight)
                                    promote.stop()
                                    controll = False
                                    break
                                elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.4*WIDTH +40 + piece_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + piece_size[1]: # Rook
                                    self.board[i][7] == 0
                                    self.board[i][7] = Rook("b", [i,7], b_rook)
                                    promote.stop()
                                    controll = False
                                    break
                                elif 0.1*WIDTH +15 < pos[0] < 0.1*WIDTH + 0.6*WIDTH +40 + piece_size[0] and 0.15*WIDTH < pos[1] < 0.15*WIDTH + piece_size[1]: # Queen
                                    self.board[i][7] == 0
                                    self.board[i][7] = Queen("b", [i,7], b_queen)
                                    promote.stop()
                                    controll = False
                                    break

