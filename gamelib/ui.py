import media
import pygame
from pygame.sprite import Sprite, Group 

class UI:
    
    def __init__(self):
        self.tiles = Group()
        self.bg = Group()
        
        self.tiles.add(Grass(96, 176, 64, 16))
        
        self.tiles.add(Grass(32, 64, 32, 16))
        self.tiles.add(Grass(192, 64, 32, 16))

        self.tiles.add(Grass(32, 224, 32, 16))
        self.tiles.add(Grass(192, 224, 32, 16))
        
        self.bg.add(TNTCrate())
        
    def update(self, tick):
        
        pass
    

class TNTCrate(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.rect = pygame.rect.Rect(96, 116, 64, 64)
        self.image = media.tntcrate.convert()
        
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
                            