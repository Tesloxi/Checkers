  
#!/usr/bin/python3
# -*- coding: utf-8 -*

"""Checkers game with pygame."""

from pygame import *
from checkers.constants import *
from checkers.game import Game

WIN = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Checkers")

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    clock = time.Clock()    
    run = True

    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            run = False
        
        for e in event.get():
            if e.type == QUIT:
                run = False

            if e.type == MOUSEBUTTONDOWN:
                pos = mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        
        game.update()

    quit()

main()