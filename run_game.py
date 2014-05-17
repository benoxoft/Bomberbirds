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
        play_demo()
    return game.ctrl.quit

while True:
    menu.reset()
    if play_demo():
        break
    game = Game(False, menu.cursor_pos + 2, screen, menu)
    game.start()
    if game.ctrl.quit:
        break
        
pygame.quit()