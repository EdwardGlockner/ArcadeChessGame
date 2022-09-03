import os
import pygame
import time
import sys 
 
from ChessBoard import Board

font_name = "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/fonts/PressStart2P-Regular.ttf"

pygame.mixer.init()
pygame.mixer.music.set_volume(0.2)
game_won_sound = pygame.mixer.Sound('/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/game_won.wav')
game_lost_sound = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/game_lost.wav")
ready_fight = pygame.mixer.Sound("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/ready-fight.mp3")
pygame.mixer.music.load("/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/Soundeffects/background_music.mp3")
pygame.mixer.music.play(-1)

def click(pos):
    x = pos[0]
    y = pos[1]
    if 0 < x < 800:
        if 0 < y < 800:
            divX = x-800
            divY = y-800
            i = int(divX / (800/8))
            j = int(divY / (800/8))
            return i+7, j+7

    return -1,-1

WIDTH = 800
HEIGHT = 800
board = pygame.transform.scale(pygame.image.load(os.path.join("img", "/Users/edward/OneDrive - Uppsala universitet/Big Python Projects/ChessGame/ChessPictures/board.png")), (WIDTH, HEIGHT))
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHESS GAME")
BOARD = Board(8,8)


def redraw_game_window():
    win.blit(board, (0,0))
    BOARD.update_legal_moves()
    BOARD.draw_board(win)
    pygame.display.update()

def end_screen(win, text):
    redraw_game_window()
    pygame.font.init()
    font1 = pygame.font.Font(font_name, 70)
    font2 = pygame.font.Font(font_name, 86)
    txt = font1.render(text,1,(255,122,36))
    txt_game_over = font2.render("GAME OVER",1,(255,122,36))
    win.blit(txt_game_over, (WIDTH/2 - txt_game_over.get_width()/2, 100))
    win.blit(txt, (WIDTH/2 - txt.get_width()/2, 300))
    pygame.display.update()
    controll = True
    if BOARD.checkmate == "w":
        game_lost_sound.play()
    else:
        game_won_sound.play()
    while controll:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                controll = False
            elif event.type == pygame.KEYDOWN:
                controll = False

ready_fight.play()

def main():
    run = True
    while run:
        old_num = BOARD.number_of_moves
        redraw_game_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
            if event.type == pygame.MOUSEMOTION:
                pass
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                BOARD.update_legal_moves()
                i,j = click(pos)
                BOARD.select_piece([i,j])
                BOARD.update_legal_moves()
                redraw_game_window()
                BOARD.promote(win)

                if BOARD.checkmate == "w":
                    end_screen(win, "BLACK WINS")
                elif BOARD.checkmate == "b":
                    end_screen(win, "WHITE WINS")

main()