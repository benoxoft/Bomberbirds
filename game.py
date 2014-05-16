import pygame

pygame.init()
pygame.mixer.init()

from gamelib.game import Game, GameControl
   
pygame.display.set_caption('Bomberbirds')
pygame.mouse.set_visible(False)

continue_playing = True
game = Game()
game.start()
pygame.quit()