import media
import pygame
from pygame.sprite import Sprite, Group 
import random
from bomb import Bomb

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
    
class MenuManager(Group):

    def __init__(self, screen):
        Group.__init__(self)
        self.screen = screen
        self.current_screen = 0
        self.cursor_pos = 0
        
    def next_screen(self):
        if self.current_screen == 2:
            return False
        self.current_screen += 1
        return True
    
    def cursor_up(self):
        self.cursor_pos -= 1
        if self.cursor_pos == -1:
            self.cursor_pos = 2
    
    def cursor_down(self):
        self.cursor_pos += 1
        if self.cursor_pos == 3:
            self.cursor_pos = 0
    
    def reset(self):
        self.current_screen = 0
        self.cursor_pos = 0
        
    def show_game_title(self):
        font = media.get_font(8)
        s = font.render("BOMBERBIRDS", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 20))
        s = font.render("entry for pyweek #18", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 30))
        s = font.render("by Benoit Paquet", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 40))

        s = font.render("music from opengameart.org", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 194))
        s = font.render("menu theme by bart", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 204))
        s = font.render("main theme by FoxSynergy", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 214))
                
    def show_demo_message(self):
        self.show_game_title()
        font = media.get_font(8)
        s = font.render("press <space> to start", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        s = font.render("press <ESC> to quit anytime", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 100))
        
    def show_menu(self):
        self.show_game_title()
        font = media.get_font(8)
        s = font.render("Select how many birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        if self.cursor_pos == 0:
            s = font.render("-> 2 birds", True, (255,255,255))
        else:
            s = font.render("   2 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 100))
        
        if self.cursor_pos == 1:
            s = font.render("-> 3 birds", True, (255,255,255))
        else:
            s = font.render("   3 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 110))
        if self.cursor_pos == 2:
            s = font.render("-> 4 birds", True, (255,255,255))
        else:
            s = font.render("   4 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 120))
    
    def show_help(self):
        self.show_game_title()
        font = media.get_font(8)
        s = font.render("You are the green bird", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        s = font.render("Use a, d and w to move", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 100))
        s = font.render("<space> create a bomb", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 110))
        s = font.render("press it again to throw it", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 120))
    
    def update(self, tick):
        if self.current_screen == 0:
            self.show_demo_message()
        elif self.current_screen == 1:
            self.show_menu()
        elif self.current_screen == 2:
            self.show_help()
            
class Minibird(Sprite):
    def __init__(self, image, x):
        Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x, 0, 8, 8)
        self.image = image.convert()
        
class LifeCounter(Group):
    def __init__(self):
        x = 8
        for i in xrange(0, 3):
            b = MiniBird(media.minibird1, x)
            x += 20
        for i in xrange(0, 3):
            b = MiniBird(media.minibird2, x)
            x += 20
        for i in xrange(0, 3):
            b = MiniBird(media.minibird3, x)
            x += 20
        for i in xrange(0, 3):
            b = MiniBird(media.minibird4, x)
            x += 20
                    
    def bird_kill(self, bird):
        pass
    
class TNTCrate(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.rect = pygame.rect.Rect(96, 112, 64, 64)
        self.image = media.tntcrate.convert()
        
    def explode(self, bird):
        for i in xrange(0, random.randint(5, 10)):
            b = Bomb(bird)
            bird.add_bomb(b)
            b.timeout = 1600
            b.rect.x = self.rect.x
            b.rect.y = self.rect.y - 32
            b.launch(random.randint(-200, 200), -random.randint(50, 300))
        self.rect = pygame.rect.Rect(10000,10000,0,0)
            
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
        Tile.__init__(self, media.grass3, x, y, h, w)
    
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
        self.image = self.star0.convert()

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
                