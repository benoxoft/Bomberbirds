import pygame
import ui
from bird import Bird

from pygame.sprite import Group

class Game:
    
    def __init__(self):
        self.ui = ui.UI()
        self.birds = Group()
        self.birds.add(Bird(1))
        self.birds.add(Bird(2))
        self.birds.add(Bird(3))
        self.birds.add(Bird(4))
        
        for b in self.birds:
            b.move.add(self.ui.tiles)
            
    def draw(self, screen, tick):
        for t in self.ui.tiles:
            screen.blit(t.image, pygame.rect.Rect(t.rect.x, t.rect.y, t.rect.w, t.rect.h))
        for b in self.birds:
            b.update(tick)
            screen.blit(b.image, pygame.rect.Rect(b.rect.x, b.rect.y, b.rect.w, b.rect.h))