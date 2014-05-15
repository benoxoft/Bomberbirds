import pygame
from gamelib.game import Game, GameControl

    
pygame.init()

pygame.display.set_caption('Bomberbirds')
pygame.mouse.set_visible(False)

continue_playing = True
game = Game()
game.start()
    