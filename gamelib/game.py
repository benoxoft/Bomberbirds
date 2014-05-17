import pygame
import ui
from bird import GreenBird, RedBird, PurpleBird, CyanBird
from brain import BirdBrain
import math
import os
import media

from pygame.sprite import Group

class GameControl:

    def __init__(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True
        self.quit = False
        self.reset_demo = False
        
    def reset(self):
        self.leftKeyDown = False
        self.rightKeyDown = False
        self.upKeyDown = False
        self.keepPlaying = True

        
class Game:
    
    def __init__(self, demo):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.demo = demo
        self.demo_timeout = 45000
        self.screen = pygame.display.set_mode((256, 240), pygame.HWSURFACE)
        self.ctrl = GameControl()
        self.clock = pygame.time.Clock()
        
        if demo:
            pygame.mixer.music.load(media.random_silly_chip_song_file)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(media.Grey_Sector_v0_86_0_file)
            pygame.mixer.music.play(-1)
            
        
        self.bg_explode = 0
        self.bg_color = (0, 0, 0)
        
        self.ui = ui.UI()
        self.birds = Group()
        self.mainchar = GreenBird(self)
        self.birds.add(self.mainchar)
        
        bird2 = RedBird(self)
        self.birds.add(bird2)
        
        bird3 = PurpleBird(self)
        self.birds.add(bird3)
        
        bird4 = CyanBird(self)
        self.birds.add(bird4)

        if demo:
            self.mainchar.brain = BirdBrain(self.mainchar, self.birds)
        bird2.brain = BirdBrain(bird2, self.birds)
        bird3.brain = BirdBrain(bird3, self.birds)
        bird4.brain = BirdBrain(bird4, self.birds)
        
        self.bombs = Group()
        
        for b in self.birds:
            b.move.add(self.ui.tiles)
        
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
        s = font.render("2 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        s = font.render("3 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        s = font.render("4 birds", True, (255,255,255))
        self.screen.blit(s, ((256 - s.get_width()) / 2, 90))
        
    def start(self):
        while self.ctrl.keepPlaying:
            for e in pygame.event.get():
                if self.demo:
                    self.manage_keys_demo(e)
                else:
                    self.manage_keys_normal(e)
                    
                if e.type == pygame.QUIT:
                    self.ctrl.keepPlaying = False
                    self.ctrl.quit = True
                    
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
            self.update(tick)
        
            pygame.display.update()
            pygame.time.delay(16)
        
        pygame.mixer.music.stop()
        
    def manage_keys_normal(self, e):
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
                self.ctrl.quit = True
            elif e.key == pygame.K_SPACE:
                self.mainchar.nuke()
    
    def manage_keys_demo(self, e):
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_ESCAPE:
                self.ctrl.keepPlaying = False  
                self.ctrl.quit = True
            elif e.key == pygame.K_SPACE:
                self.ctrl.keepPlaying = False  
    
    def add_bomb_event(self, bomb):
        self.bombs.add(bomb)
        bomb.explode_event = self.explode_event
        bomb.delete_bomb = self.delete_bomb
        
    def explode_event(self, bomb):
        self.bg_explode = 10

        distance = math.sqrt(
                             abs(bomb.rect.centerx - self.ui.tntcrate.rect.centerx)**2 +
                             abs(bomb.rect.centery - self.ui.tntcrate.rect.centery)**2)
        if distance <= 56:
            self.ui.tntcrate.explode(bomb.bird)
            
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
                
    def kill_event(self, bird):
        pass#self.lives.remove_life(bird)
                
    def delete_bomb(self, bomb):
        self.bombs.remove(bomb)
                
    def update(self, tick):
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
                if b is bomb.bird or b.dead:
                    continue
                distance = math.sqrt(
                                     abs(bomb.rect.centerx - b.rect.centerx)**2 +
                                     abs(bomb.rect.centery - b.rect.centery)**2)                
                if distance <= 8:
                    bomb.explode()
        if self.demo:
            self.demo_timeout -= tick
            if self.demo_timeout < 0:
                self.ctrl.keepPlaying = False
                self.ctrl.reset_demo = True
            self.show_demo_message()
            