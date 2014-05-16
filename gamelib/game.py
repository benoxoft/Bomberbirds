import pygame
import ui
from bird import Bird
from brain import BirdBrain
import math
import os

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
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen = pygame.display.set_mode((256, 240))
        self.ctrl = GameControl()
        self.clock = pygame.time.Clock()

        self.bg_explode = 0
        self.bg_color = (0, 0, 0)
        
        self.ui = ui.UI()
        self.birds = Group()
        self.mainchar = Bird(1, self.add_bomb)
        self.birds.add(self.mainchar)
        
        bird2 = Bird(2, self.add_bomb)
        self.birds.add(bird2)
        
        bird3 = Bird(3, self.add_bomb)
        self.birds.add(bird3)
        
        bird4 = Bird(4, self.add_bomb)
        self.birds.add(bird4)

        #self.mainchar.brain = BirdBrain(self.mainchar, self.birds)
        bird2.brain = BirdBrain(bird2, self.birds)
        bird3.brain = BirdBrain(bird3, self.birds)
        bird4.brain = BirdBrain(bird4, self.birds)
        
        self.bombs = Group()
        
        for b in self.birds:
            b.move.add(self.ui.tiles)
        
    def start(self):
        
        while self.ctrl.keepPlaying:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_a:
                        self.ctrl.leftKeyDown = True
                    elif e.key == pygame.K_d:
                        self.ctrl.rightKeyDown = True
                    elif e.key == pygame.K_w:
                        self.ctrl.upKeyDown = True
                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_a:
                        self.ctrl.leftKeyDown = False
                    elif e.key == pygame.K_d:
                        self.ctrl.rightKeyDown = False
                    elif e.key == pygame.K_w:
                        self.ctrl.upKeyDown = False
                    elif e.key == pygame.K_ESCAPE:
                        self.ctrl.keepPlaying = False  
                    elif e.key == pygame.K_SPACE:
                        self.mainchar.nuke()
                elif e.type == pygame.QUIT:
                    self.ctrl.keepPlaying = False
            if self.ctrl.leftKeyDown:
                self.mainchar.moveleft(tick)
            if self.ctrl.rightKeyDown:
                self.mainchar.moveright(tick)
            if self.ctrl.upKeyDown:
                self.mainchar.thrust(tick)
            tick = self.clock.tick()
            
            if self.bg_explode > 0:
                if self.bg_explode % 2 == 0:
                    self.bg_color = (255, 255, 255)
                else:
                    self.bg_color = (0, 0, 0)
                self.bg_explode -= 1
            elif self.bg_explode == 1:
                self.bg_explode = 0
                self.bg_color = (0, 0, 0)
                
            self.screen.fill(self.bg_color)
            self.draw(tick)
        
            pygame.display.update()
            pygame.time.delay(16)
        
    def add_bomb(self, bomb):
        self.bombs.add(bomb)
        bomb.explode_event = self.explode_event
        bomb.delete_bomb = self.delete_bomb
        
    def explode_event(self, bomb):
        self.bg_explode = 10

        distance = math.sqrt(
                             abs(bomb.rect.centerx - self.ui.tntcrate.rect.centerx)**2 +
                             abs(bomb.rect.centery - self.ui.tntcrate.rect.centery)**2)
        if distance <= 56:
            self.ui.tntcrate.explode()
            
        for b in self.bombs:
            if b is bomb:
                continue
            distance = math.sqrt(
                                 abs(bomb.rect.centerx - b.rect.centerx)**2 +
                                 abs(bomb.rect.centery - b.rect.centery)**2)
            if distance <= 24 and not b.exploded:
                b.explode()
                
        for b in self.birds:
            distance = math.sqrt(
                                 abs(bomb.rect.centerx - b.rect.centerx)**2 +
                                 abs(bomb.rect.centery - b.rect.centery)**2)

            if distance <= 24:
                b.kill()
                        
    def delete_bomb(self, bomb):
        self.bombs.remove(bomb)
                
    def draw(self, tick):
        for t in self.ui.bg:
            t.update(tick)
            self.screen.blit(t.image, pygame.rect.Rect(t.rect.x, t.rect.y, t.rect.w, t.rect.h))

        for t in self.ui.tiles:
            self.screen.blit(t.image, pygame.rect.Rect(t.rect.x, t.rect.y, t.rect.w, t.rect.h))
        
        for b in self.birds:
            b.update(tick)
            self.screen.blit(b.image, pygame.rect.Rect(b.rect.x, b.rect.y, b.rect.w, b.rect.h))
            
        for bomb in self.bombs:
            bomb.update(tick)
            self.screen.blit(bomb.image, pygame.rect.Rect(bomb.rect.x, bomb.rect.y, bomb.rect.w, bomb.rect.h))
            
            if bomb.attached:
                continue
            
            for b in self.birds:
                if b is bomb.bird:
                    continue
                distance = math.sqrt(
                                     abs(bomb.rect.centerx - b.rect.centerx)**2 +
                                     abs(bomb.rect.centery - b.rect.centery)**2)                
                if distance <= 8:
                    bomb.explode()

            