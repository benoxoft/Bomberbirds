
import pygame
import os
import sys

def load_image(img):
    return pygame.image.load(img)

m = sys.modules[__name__]
for f in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'media')):
    filename, _ = os.path.splitext(f)
    fullf = os.path.abspath(os.path.join('media', f))
    print fullf
    setattr(m, filename, load_image(fullf))

