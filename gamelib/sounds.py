
import pygame
import os
import sys

def load_sound(img):
    return pygame.mixer.Sound(img)

m = sys.modules[__name__]
for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'sound')):
    filename, _ = os.path.splitext(f)
    fullf = os.path.abspath(os.path.join('sound', f))
    print fullf
    setattr(m, filename, load_sound(fullf))

