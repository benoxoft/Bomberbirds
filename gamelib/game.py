#! /usr/bin/env python

#    Copyright (C) 2014  Benoit <benoxoft> Paquet
#
#    This file is part of Bomberbirds.
#
#    Bomberbirds is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame
import ui
from birds import GreenBird, RedBird, PurpleBird, CyanBird
from brain import BirdBrain
import math
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
    
    def __init__(self, 
                 demo, 
                 birds, 
                 screen,
                 menu):
        self.demo = demo
        self.demo_timeout = 45000
        self.screen = screen
        self.ctrl = GameControl()
        self.clock = pygame.time.Clock()
        self.menu = menu
        self.menu.cursor_pos = 0
        
        if demo:
            pygame.mixer.music.load(media.random_silly_chip_song_file)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load(media.Grey_Sector_v0_86_0_file)
            pygame.mixer.music.play(-1)
        
        self.bg_explode = 0
        self.bg_color = (0, 0, 0)
        
        self.ui = ui.UI()
        self.birds = []
        self.mainchar = GreenBird(self)
        self.birds.append(self.mainchar)
        
        bird2 = RedBird(self)
        self.birds.append(bird2)
        
        if birds >= 3:
            bird3 = PurpleBird(self)
            self.birds.append(bird3)
        
        if birds == 4:
            bird4 = CyanBird(self)
            self.birds.append(bird4)

        if demo:
            self.mainchar.brain = BirdBrain(self.mainchar, self.birds)
            
        bird2.brain = BirdBrain(bird2, self.birds)
        if birds >= 3:
            bird3.brain = BirdBrain(bird3, self.birds)
        if birds == 4:
            bird4.brain = BirdBrain(bird4, self.birds)
        
        self.bombs = Group()
        
        for b in self.birds:
            b.move.add(self.ui.tiles)
        
        self.lives = ui.LifeCounter(self.birds, self.screen)

    def start(self):
        while self.ctrl.keepPlaying:
            for e in pygame.event.get():
                if self.demo or self.menu.game_over:
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
                if not self.menu.next_screen() or self.menu.game_over != 0:
                    self.ctrl.keepPlaying = False
            elif e.key == pygame.K_UP or e.key == pygame.K_w:
                self.menu.cursor_up()
            elif e.key == pygame.K_DOWN or e.key == pygame.K_s:
                self.menu.cursor_down()
    
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
            if b.counter_invincible <= 0 or not b.invisible:
                self.screen.blit(b.image, pygame.rect.Rect(b.rect.x, b.rect.y, b.rect.w, b.rect.h))
            b.invisible = not b.invisible
            
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
            self.menu.update(tick)
            self.demo_timeout -= tick
            if self.demo_timeout < 0:
                self.ctrl.keepPlaying = False
                self.ctrl.reset_demo = True
        else:
            self.lives.update(tick)
            if self.mainchar.lives == 0:
                self.menu.game_over = 1
                self.menu.update(tick)
            alives = 0
            for b in self.birds:
                if b.lives > 0:
                    alives += 1 
            if alives == 1 and self.mainchar.lives > 0:
                self.menu.game_over = 2
                self.menu.update(tick)
            elif alives == 0:
                self.menu.game_over = 3
                self.menu.update(tick)
