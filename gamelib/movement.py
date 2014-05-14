#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright (C) 2010  Benoit <benoxoft> Paquet
#
#    This program is free software: you can redistribute it and/or modify
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

from pygame.sprite import Group
from pygame.rect import Rect

import math

class Movement(Group):
    def  __init__(self, moving_sprite,
                  speedx = 0,
                  maxspeedx = -1,
                  speedy = 0,
                  maxspeedy = -1,
                  posx = 0,
                  posy = 0,
                  thrust_strength = 0,
                  accelx = 0,
                  accely = 0,
                  gravity = 1000):
        Group.__init__(self)
        self.moving_sprite = moving_sprite
        self.speedx = speedx
        self.speedy = speedy
        self.maxspeedx = maxspeedx
        self.maxspeedy = maxspeedy
        self.posx = posx
        self.posy = posy
        self.thrust_strength = thrust_strength
        self.accelx = accelx
        self.accely = accely
        self.gravity = gravity
        self.bumping_walls = []
        
    def get_speed(self):
        return math.sqrt(self.speedx**2 + self.speedy**2)
    
    def thrust(self, tick):
        self.speedy -= self.thrust_strength * tick / 1000.0
        if self.maxspeedy != -1 and abs(self.speedy) > self.maxspeedy:
            self.speedy = -self.maxspeedy
        
    def moveleft(self, tick):
        self.speedx -= self.accelx * tick / 1000.0
        if self.maxspeedx != -1 and abs(self.speedx) > self.maxspeedx:
            self.speedx = -self.maxspeedx
        
    def moveright(self, tick):
        self.speedx += self.accelx * tick / 1000.0
        if self.maxspeedx != -1 and self.speedx > self.maxspeedx:
            self.speedx = self.maxspeedx

    def movedown(self, tick):
        self.speedy += self.accely * tick / 1000.0
        if self.maxspeedy != -1 and abs(self.speedy) > self.maxspeedy:
            self.speedy = self.maxspeedy
    
    def calculate_movement(self, tick):
        self.speedy += self.gravity * tick / 1000.0
        if self.maxspeedy != -1 and self.speedy > self.maxspeedy:
            self.speedy = self.maxspeedy
        self.check_collision(tick)
        self.posy = self.get_new_posy(tick)
        self.posx = self.get_new_posx(tick)

    def get_new_posx(self, tick):
        return self.posx + self.speedx * tick / 1000.0

    def get_new_posy(self, tick):
        return self.posy + self.speedy * tick / 1000.0

    def check_collision(self, tick):
        oldrect = self.moving_sprite.rect
        newrect = Rect(self.get_new_posx(tick), self.get_new_posy(tick), oldrect.width, oldrect.height)
        collisions = [col for col in self.sprites() if col.rect.colliderect(newrect)]
        if len(collisions) > 0:
            for coll in collisions:
                col = coll.rect
                if newrect.right >= col.x and oldrect.right <= col.x:
                    self.posx = col.x - oldrect.width
                    self.speedx = 0
                if newrect.x <= col.right and oldrect.x >= col.right:
                    self.posx = col.right
                    self.speedx = 0
                if newrect.bottom >= col.y and oldrect.bottom <= col.y:
                    self.posy = col.y - oldrect.height
                    self.speedy = 0
                    self.speedx /= 1.2
                    if self.speedx < 1 and self.speedx > -1:
                        self.speedx = 0
                if newrect.y <= col.bottom and oldrect.y >= col.bottom:
                    self.posy = col.bottom
                    self.speedy = 0
                    self.speedx /= 1.1
                    if self.speedx < 1 and self.speedx > -1:
                        self.speedx = 0

        self.bumping_walls = collisions
        
    def check_collision_x(self, tick):
        collisions = []
        newposx = self.get_new_posx(tick)
        if self.speedx > 0:
            currentposx = self.moving_sprite.rect.right
            newposx += + self.moving_sprite.rect.width
            possible_cols = [col for col in self.sprites()
                             if col.rect.x >= currentposx and col.rect.x <= newposx]
            for spr in possible_cols:
                dist = abs(spr.rect.right - currentposx)
                t = float(dist/abs(self.speedx))
                ypos = self.get_new_posy(t)
                if ypos <= spr.rect.bottom and ypos >= spr.rect.top:
                    collisions.append((t, spr.rect.x - self.moving_sprite.rect.width))
        elif self.speedx < 0:
            possible_cols = [col for col in self.sprites()
                if col.rect.right <= self.posx and col.rect.right >= newposx]
            for spr in possible_cols:
                dist = abs(spr.rect.right - self.posx)
                t = float(dist/abs(self.speedx))
                ypos = self.get_new_posy(t)
                if ypos <= spr.rect.bottom and ypos >= spr.rect.top:
                    collisions.append((t, spr.rect.right))
        if len(collisions) == 0:
            return tick
        else:
            self.speedx = 0
            first_col = tick
            for t,x in collisions:
                if t < first_col:
                    first_col = t
                    self.posx = x
            return tick - first_col
        
    def check_collision_y(self, tick):
        collisions = []
        newposy = self.get_new_posy(tick)

        if self.speedy > 0:
            currentposy = self.posy + self.moving_sprite.rect.height
            newposy += self.moving_sprite.rect.height
            possible_cols = [col for col in self.sprites()
                             if col.rect.top >= currentposy and col.rect.top <= newposy]
            for spr in possible_cols:
                dist = abs(spr.rect.top - currentposy)
                t = float(dist/abs(self.speedy))
                xpos = self.get_new_posx(t)
                if xpos <= spr.rect.right and xpos >= spr.rect.x:
                    collisions.append((t, spr.rect.top - self.moving_sprite.rect.height))
        elif self.speedy < 0:            
            possible_cols = [col for col in self.sprites()
                             if col.rect.bottom <= self.posy and col.rect.bottom >= newposy]
            for spr in possible_cols:
                dist = abs(spr.rect.bottom - self.posy)
                t = float(dist/abs(self.speedy))
                xpos = self.get_new_posx(t)
                if xpos <= spr.rect.right and xpos >= spr.rect.x:
                    collisions.append((t, spr.rect.bottom))

        if len(collisions) == 0:
            return tick
        else:
            self.speedy = 0
            self.speedx /= 1.2
            if self.speedx < 1 and self.speedx > -1:
                self.speedx = 0
            first_col = tick
            for t,y in collisions:
                if t < first_col:
                    first_col = t
                    self.posy = y
            return tick - first_col