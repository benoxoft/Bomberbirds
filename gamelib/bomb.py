from pygame.sprite import Sprite, Group
from movement import Movement

import pygame
import math
import media
import sounds

class Bomb(Sprite):
    
    def __init__(self, bird):
        Sprite.__init__(self)
        sounds.bomb.play()
        self.bird = bird
        self.bomb = media.bomb.convert()
        self.bomb2 = media.bomb2.convert()
        self.boom = media.boom.convert()        
        self.rect = pygame.rect.Rect(self.bird.rect.x, bird.rect.y + 16, 16, 16)
        self.image = self.bomb
        self.move = Movement(self,
                             accelx = 1000,
                             accely = 1000,
                             maxspeedx = 200,
                             maxspeedy = 200,
                             gravity = 1000,
                             decrease_speed_ratio = 2                        
                             )
        self.move.add(self.bird.move.sprites())
        self.timeout = 3400
        self.explode_event = None
        self.delete_bomb = None
        self.exploded = False
        self.bombstate = 4
        self.attached = True
        
    def launch(self, speedx, speedy):
        self.attached = False
        sounds.throw.play()
        self.move.speedx = speedx * 2
        self.move.speedy = speedy * 2
        self.move.posx = self.rect.x
        self.move.posy = self.rect.y
        
    def explode(self):
        self.timeout = 400
        self.exploded = True
        self.explode_event(self)
        sounds.explode.play()
        self.attached = False
        self.rect.height = 64
        self.rect.width = 64
        self.rect.x -= 16
        self.rect.y -= 16
        self.image = self.boom
        
    def update(self, tick):
            
        self.timeout -= tick
        if 400 < self.timeout < 800:
            if self.bombstate == 4:
                self.image = self.bomb2
            elif self.bombstate == 2:
                self.image = self.bomb
            self.bombstate -= 1
            if self.bombstate == 0:
                self.bombstate = 4
                
        if self.timeout < 400 and not self.exploded:
            self.explode()
        if self.timeout < 0:
            self.delete_bomb(self)
            
        if self.attached:
            self.rect.x = self.bird.rect.x
            self.rect.y = self.bird.rect.y + 16
        elif not self.exploded:
            self.move.calculate_movement(tick)
    
            self.rect.x = self.move.posx
            self.rect.y = self.move.posy
