import pygame
import ui

class Game:
    
    def __init__(self):
        self.ui = ui.UI()
        
    def draw(self, screen, tick):
        for t in self.ui.tiles:
            screen.blit(t.image, pygame.rect.Rect(t.rect.x, t.rect.y, t.rect.w, t.rect.h))
