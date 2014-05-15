import pygame
from gamelib.game import Game

    
pygame.init()

screen = pygame.display.set_mode((256, 240))

pygame.display.set_caption('Bomberbirds')
pygame.mouse.set_visible(False)

continue_playing = True
game = Game()
clock = pygame.time.Clock()

while continue_playing:
    tick = clock.tick()
    screen.fill((0,0,0))
    game.draw(screen, tick)
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            pass
        elif e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                continue_playing = False
        pygame.display.update()
        pygame.time.delay(10)
        
    
    