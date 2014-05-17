from pygame.sprite import Sprite, Group
from movement import Movement
from bomb import Bomb

import pygame
import math
import media

class Bird(Sprite):
    
    def __init__(self,
                 bird,
                 birdflyup,
                 birdflydown,
                 initx,
                 inity, 
                 init_dir,
                 add_bomb):
        Sprite.__init__(self)
        
        self.imgflip = init_dir == -1
        self.wing = 0 
        self.has_bomb = False
        self.bomb = None
        self.add_bomb = add_bomb
        self.dead = False
        self.brain = None

        self.bird = bird
        self.birdflyup = birdflyup
        self.birdflydown = birdflydown
        self.initx = initx
        self.inity = inity
        self.dir = init_dir

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
        elif self.wing == 6:
            self.image = self.birdflyup
            self.flyup = True
            self.imgflip = False
            self.flip()
        elif self.wing > 6:
            self.wing = 0
            
        self.firstupdate = True
        self.move.thrust(tick)
        
    def kill(self):
        self.dead = True
        media.kill.play()
        
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

        self.rect.x = self.move.posx
        self.rect.y = self.move.posy

    def raise_no_more_life_event(self):
        self.no_more_life_event()

    def remove_life(self):
        self.lives -= 1
        if self.lives == 0:
            self.raise_no_more_life_event()
        
class GreenBird(Bird):
    def __init__(self, add_bomb):
        Bird.__init__(self,
                      media.bird1,
                      media.birdflyup1,
                      media.birdflydown1,
                      32,
                      32,
                      1,
                      add_bomb)

class RedBird(Bird):
    def __init__(self, add_bomb):
        Bird.__init__(self,
                      media.bird2,
                      media.birdflyup2,
                      media.birdflydown2,
                      192,
                      32,
                      -1, 
                      add_bomb)

class PurpleBird(Bird):
    def __init__(self, add_bomb):
        Bird.__init__(self,
                      media.bird3,
                      media.birdflyup3,
                      media.birdflydown3,
                      32,
                      192,
                      1,
                      add_bomb)

class CyanBird(Bird):
    def __init__(self, add_bomb):
        Bird.__init__(self,
                      media.bird4,
                      media.birdflyup4,
                      media.birdflydown4,
                      192,
                      192,
                      -1, 
                      add_bomb)
