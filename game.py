import pygame
       
def main():
    pygame.init()
    
    screen = pygame.display.set_mode((800, 600))

    pygame.display.set_caption('Bomberbirds')
    pygame.mouse.set_visible(False)

    continue_playing = True
    while continue_playing:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                pass
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    continue_playing = False
            pygame.time.delay(10)
        
if __name__ == '__main__':
    main()
    