from pygame.sprite import Sprite, Group
from movement import Movement
from bomb import Bomb

import pygame
import math
import media
import sounds

class Bird(Sprite):
    
    def __init__(self, birdno, add_bomb):
        Sprite.__init__(self)
        
        self.imgflip = False
        self.dir = 1
        self.wing = 0 
        self.has_bomb = False
        self.bomb = None
        self.add_bomb = add_bomb
        self.dead = False
        self.brain = None
        
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
            self.inity = 192
        else:
            self.bird = media.bird4
            self.birdflyup = media.birdflyup4
            self.birdflydown = media.birdflydown4
            self.initx = 192
            self.inity = 192
            self.imgflip = True
            self.dir = -1

        self.move = Movement(self, 
                             thrust_strength = 1000,
                             accelx = 700,
                             accely = 200,
                             maxspeedx = 120,
                             maxspeedy = 160,
                             gravity = 400,
                             posx=self.initx,
                             posy=self.inity)
            
        self.deadbird = media.deadbird
        
        self.firstupdate = False
        self.image = self.bird
        self.rect = self.image.get_rect()
        self.rect.width /= 2
        self.rect.height -= 4
        self.lives = 3
        
        self.no_more_life_event = None

    def set_init_pos(self):
        self.move.posx = self.initx
        self.move.posy = self.inity
        self.move.speedx = 0
        self.move.speedy = 0
        self.dir = 1
        self.flip()
        
    def nuke(self):
        if self.dead:
            return
        
        if not self.has_bomb:
            self.create_bomb()
            self.has_bomb = True
        else:
            self.throw_bomb()
    
    def create_bomb(self):
        self.bomb = Bomb(self)
        self.add_bomb(self.bomb)
        
    def throw_bomb(self):
        self.has_bomb = False
        self.bomb.launch(self.move.speedx, self.move.speedy)
    
    def flip(self):
        if not self.imgflip and self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = True
        elif self.imgflip and self.dir == 1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.imgflip = False
        
    def moveleft(self, tick):
        if self.dead:
            return
        
        self.dir = -1
        self.flip()

        self.move.moveleft(tick)
        
    def moveright(self, tick):
        if self.dead:
            return
        
        self.dir = 1
        self.flip()
        #if self.move.speedy == 0:
        self.move.moveright(tick)
        
    def thrust(self, tick):
        if self.dead:
            return
        
        self.wing += 1
        if self.wing == 3:
            self.image = self.birdflydown
            self.flyup = False
            self.imgflip = False
            self.flip()
            sounds.flap1.play()
        elif self.wing == 6:
            self.image = self.birdflyup
            self.flyup = True
            self.imgflip = False
            self.flip()
            sounds.flap2.play()            
        elif self.wing > 6:
            self.wing = 0
            
        self.firstupdate = True
        self.move.thrust(tick)
        
    def kill(self):
        self.dead = True
        sounds.kill3.play()
        
    def update(self, tick):
        if self.brain is not None:
            self.brain.update(tick)

        if not self.firstupdate:
            if self.dead:
                self.image = self.deadbird
            else:
                self.image = self.bird
            self.imgflip = False
            self.flip()
        self.firstupdate = False
        
        self.move.calculate_movement(tick)

        #if self.move.speedx > 0:
        #    self.move.speedx -= 1
        #elif self.move.speedx < 0:
        #    self.move.speedx += 1
            
        self.rect.x = self.move.posx
        self.rect.y = self.move.posy

    def raise_no_more_life_event(self):
        self.no_more_life_event()

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.raise_no_more_life_event()
        
