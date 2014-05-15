import pygame
import ui
from bird import Bird

from pygame.sprite import Group

class GameControl:

    def __init__(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True

    def reset(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True

        
class Game:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((256, 240))
        self.ctrl = GameControl()
        self.clock = pygame.time.Clock()

        self.ui = ui.UI()
        self.birds = Group()
        self.mainchar = Bird(1)
        self.birds.add(self.mainchar)
        self.birds.add(Bird(2))
        self.birds.add(Bird(3))
        self.birds.add(Bird(4))
        for b in self.birds:
            b.move.add(self.ui.tiles)
        
    def start(self):
        
        while self.ctrl.keepPlaying:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        self.ctrl.leftKeyDown = True
                    elif e.key == pygame.K_RIGHT:
                        self.ctrl.rightKeyDown = True
                    elif e.key == pygame.K_SPACE:
                        self.ctrl.upKeyDown = True
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT:
                        self.ctrl.leftKeyDown = False
                    elif e.key == pygame.K_RIGHT:
                        self.ctrl.rightKeyDown = False
                    elif e.key == pygame.K_SPACE:
                        self.ctrl.upKeyDown = False
                    elif e.key == pygame.K_ESCAPE:
                        self.ctrl.keepPlaying = False  
        
            if self.ctrl.leftKeyDown:
                self.mainchar.moveleft(tick)
            if self.ctrl.rightKeyDown:
                self.mainchar.moveright(tick)
            if self.ctrl.upKeyDown:
                self.mainchar.thrust(tick)
            tick = self.clock.tick()
            self.screen.fill((0,0,0))
            self.draw(tick)
        
            pygame.display.update()
            pygame.time.delay(16)
        
    def draw(self, tick):
        for t in self.ui.tiles:
            self.screen.blit(t.image, pygame.rect.Rect(t.rect.x, t.rect.y, t.rect.w, t.rect.h))
        for b in self.birds:
            b.update(tick)
            self.screen.blit(b.image, pygame.rect.Rect(b.rect.x, b.rect.y, b.rect.w, b.rect.h))
            