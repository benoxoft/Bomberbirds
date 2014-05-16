import media
import pygame
from pygame.sprite import Sprite, Group 
import random

class UI:
    
    def __init__(self):
        self.tiles = Group()
        self.bg = Group()
        self.tntcrate = TNTCrate()
        
        self.tiles.add(Grass(96, 176, 64, 16))
        
        self.tiles.add(Grass(32, 64, 32, 16))
        self.tiles.add(Grass(192, 64, 32, 16))

        self.tiles.add(Grass(32, 224, 32, 16))
        self.tiles.add(Grass(192, 224, 32, 16))

        for i in xrange(0, 50):
            self.bg.add(Star())

        self.bg.add(self.tntcrate)
        
    def update(self, tick):
        pass
    

class TNTCrate(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.rect = pygame.rect.Rect(96, 112, 64, 64)
        self.image = media.tntcrate.convert()
        
    def explode(self):
        pass
            
    def update(self, tick):
        pass
    
class Tile(Sprite):
    
    def __init__(self, image, x, y, h, w):
        Sprite.__init__(self)
        tile = image.convert()
        rtile = tile.get_rect()
        self.rect = pygame.rect.Rect(x, y, h, w)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
                        
        columns = int(self.rect.width / rtile.width) + 1
        rows = int(self.rect.height / rtile.height) + 1
        
        for y in xrange(rows):
            for x in xrange(columns):
                if x == 0 and y > 0:
                    rtile = rtile.move([-(columns -1 ) * rtile.width, rtile.height])
                if x > 0:
                    rtile = rtile.move([rtile.width, 0])
                self.image.blit(tile, rtile)

class Grass(Tile):    
    def __init__(self, x, y, h, w):
        Tile.__init__(self, media.grass2, x, y, h, w)
    
class Dirt(Tile):
    def __init__(self, x, y, h, w):
        Tile.__init__(self, media.dirt, x, y, h, w)
        
class Water(Tile):
    def __init__(self, x, y, h, w):
        Tile.__init__(self, media.water, x, y, h, w)
         
class Star(Sprite):
    
    def __init__(self):
        Sprite.__init__(self)
        self.rect = pygame.rect.Rect(random.randint(16, 240), random.randint(16, 224), 16, 16)
        self.star0 = media.star0.convert()
        self.star1 = media.star1.convert()
        self.star2 = media.star2.convert()
        self.star3 = media.star3.convert()
        self.current_star = random.randint(0, 10)
        self.image = self.star0

        self.next_update = 0
        
    def update(self, tick):
        self.next_update -= tick
        
        if self.next_update < 0:
            self.next_update = random.randint(500, 2000)
            if self.current_star == 0:
                self.image = self.star1
            elif self.current_star == 1:
                self.image = self.star2
            elif self.current_star == 2:
                self.image = self.star3
            elif self.current_star == 3:
                self.image = self.star2
            elif self.current_star == 4:
                self.image = self.star1
            elif self.current_star < 10:
                self.image = self.star0
            else:
                self.current_star = -1
            self.current_star += 1
                