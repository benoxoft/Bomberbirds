import pygame
pygame.init()
pygame.mixer.init()

from gamelib.game import Game, GameControl
from gamelib.ui import MenuManager
   
pygame.display.set_caption('BOMBERBIRDS')
pygame.mouse.set_visible(False)

import os
os.environ['SDL_VIDEO_CENTERED'] = '1'

screen = pygame.display.set_mode((256, 240), pygame.HWSURFACE)
menu = MenuManager(screen)

def play_demo():
    game = Game(True, 4, screen, menu)
    game.start()
    if game.ctrl.reset_demo:
        return play_demo()
    menu.birds = menu.cursor_pos + 2
    return game.ctrl.quit

def play_game():
    game = Game(False, menu.birds, screen, menu)
    game.start()
    return game.ctrl.quit

while True:
    if menu.game_over:
        if menu.cursor_pos == 0:
            menu.reset()
            if play_game():
                break
        elif menu.cursor_pos == 1:
            menu.reset()
        elif menu.cursor_pos == 2:
            break
    else:
        menu.reset()
        if play_demo():
            break
        if play_game():
            break
        
pygame.quit()