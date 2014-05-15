from pygame.sprite import Sprite, Group
from movement import Movement

import pygame
import math
import media

class Bird(Sprite):
    
    
    def __init__(self, birdno):
        Sprite.__init__(self)
        
        self.imgflip = False
        self.dir = 1
        self.wing = 0 

        if birdno == 1:
            self.bird = media.bird1
            self.birdflyup = media.birdflyup1
            self.birdflydown = media.birdflydown1
            self.initx = 32
            self.inity = 32
        elif birdno == 2:
            self.bird = media.bird2
            self.birdflyup = media.birdflyup2
            self.birdflydown = media.birdflydown2
            self.initx = 192
            self.inity = 32
            self.imgflip = True
            self.dir = -1
        elif birdno == 3:
            self.bird = media.bird3
            self.birdflyup = media.birdflyup3
            self.birdflydown = media.birdflydown3
            self.initx = 32
            self.inity = 96
        else:
            self.bird = media.bird4
            self.birdflyup = media.birdflyup4
            self.birdflydown = media.birdflydown4
            self.initx = 192
            self.inity = 96
            self.imgflip = True
            self.dir = -1


        self.move = Movement(self, 
                             thrust_strength = 0,
                             accelx = 1000,
                             accely = 1000,
                             maxspeedx = 120,
                             maxspeedy = 120,
                             gravity = 1000,
                             posx=self.initx,
                             posy=self.inity)
            
        self.deadbird = media.deadbird
        
        self.firstupdate = False
        self.image = self.bird
        self.rect = self.image.get_rect()
        self.lives = 3
        
        self.no_more_life_event = None

    def set_init_pos(self):
        self.move.posx = self.initx
        self.move.posy = self.inity
        self.move.speedx = 0
        self.move.speedy = 0
        self.dir = 1
        self.flip()
        
    def flip(self):
        if not self.imgflip and self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = True
        elif self.imgflip and self.dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = False
        
    def moveleft(self, tick):
        self.dir = -1
        self.flip()

        #if self.move.speedy == 0:
        self.move.moveleft(tick)
        
    def moveright(self, tick):
        self.dir = 1
        self.flip()
        #if self.move.speedy == 0:
        self.move.moveright(tick)
        
    def thrust(self, tick):
        self.wing += 1
        if self.wing == 3:
            self.image = self.birdflydown
            self.flyup = False
            self.imgflip = False
            self.flip()
        elif self.wing == 6:
            self.image = self.birdflyup
            self.flyup = True
            self.imgflip = False
            self.flip()
            
        elif self.wing > 6:
            self.wing = 0
            
        self.firstupdate = True
        self.move.thrust(tick)
        
    def update(self, tick):
        if not self.firstupdate:
            self.image = self.bird
            self.imgflip = False
            self.flip()
        self.firstupdate = False
        
        self.move.calculate_movement(tick)

        if self.move.speedx > 0:
            self.move.speedx -= 1
        elif self.move.speedx < 0:
            self.move.speedx += 1
            
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy

    def raise_no_more_life_event(self):
        self.no_more_life_event()

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.raise_no_more_life_event()
        
