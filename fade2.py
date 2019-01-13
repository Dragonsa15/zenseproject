import sys
import time
import pygame

fadingin = 50
fadingout = 5

def text_objects(text, font):
    textSurface = font.render(text, True,(255,255,255))
    return textSurface, textSurface.get_rect()

def fadeinmethodtext(screen,width,height):
    TextType = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, text_rect = text_objects("Star Formation", TextType)
    text_rect.center = (width/2,height/2 - 20)    
    fadeinstate = 0
    state = 0
    state_stage = 0

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                quit()
        state_stage += 0.05

        if state == fadeinstate:
            if state_stage >= fadingin:
                return 0
        else:
            pygame.quit()
            quit()
        
        if state == fadeinstate:
            alpha = 1.0 * state_stage / fadingin
            rt = TextSurf
        else:
            pygame.quit()
            quit()

        surf2 = pygame.surface.Surface((text_rect.width, text_rect.height))
        surf2.set_alpha(255 * alpha)
        screen.fill((0, 0, 0))
        surf2.blit(rt, (0, 0))
        screen.blit(surf2, text_rect)
    
        pygame.display.flip()
        
                
