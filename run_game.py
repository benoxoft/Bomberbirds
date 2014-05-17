import pygame

pygame.init()
pygame.mixer.init()

from gamelib.game import Game, GameControl
   
pygame.display.set_caption('BOMBERBIRDS')
pygame.mouse.set_visible(False)

def play_demo():
    game = Game(True)
    game.start()
    if game.ctrl.reset_demo:
        play_demo()
    return game.ctrl.quit

while True:
    if play_demo():
        break
    game = Game(False)
    game.start()
    if game.ctrl.quit:
        break
        
pygame.quit()