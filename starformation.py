import random
import pygame
import PyParticles
import sys
import fade2

pygame.init()

red = (200,0,0)
green = (0,200,0)
clock = pygame.time.Clock()
instructions = pygame.image.load("NewProject.jpg")
instructions = pygame.transform.scale(instructions,(800,700))
pygame.mixer.music.load("intro.mp3")
       

bright_red = (255,0,0)
bright_green = (0,255,0)

def calculateRadius(mass):
    return 0.5 * mass ** (0.5)

(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Star formation')
screen.set_alpha(0)

universe = PyParticles.Environment(width, height)
universe.colour = (0,0,0)
universe.addFunctions(['move', 'attract', 'combine'])
universe_screen = PyParticles.UniverseScreen(width, height)

def text_objects(text, font):
    textSurface = font.render(text, True,(255,255,255))
    return textSurface, textSurface.get_rect()

def intro(flag = 1):
    pygame.mixer.music.play(-1)
    intro = True
    instructions_state = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((0,0,0))
        TextType = pygame.font.Font('freesansbold.ttf',100)
        TextSurf, TextRect = text_objects("Star Formation", TextType)
        TextRect.center = (width/2,height/2 - 20)
        if(flag==1):
            flag = fade2.fadeinmethodtext(screen,width,height)

        screen.blit(TextSurf, TextRect)
        TextType2 = pygame.font.Font('freesansbold.ttf',25)
        Text2, TextRect2 = text_objects("Start", TextType2)
        TextRect2.center = ((50+140)/2,500+30)
        
              
  
        Text3, TextRect3 = text_objects("Quit", TextType2)
        TextRect3.center = (550+(150+150)/2,500+30)
        
        
        Text4, TextRect4 = text_objects("Instrutions", TextType2)
        TextRect4.center = (330+(145)/2,500+30)
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if 50+100 > mouse[0] > 50 and 500 + 60 > mouse[1] > 500:
            pygame.draw.rect(screen, bright_green,(50,500,100,60),1)
            screen.blit(Text2, TextRect2)
            if(click[0]==1):
                simulation()
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, red,(50,500,100,60),1)
        if 650+100 > mouse[0] > 650 and 500 + 60 > mouse[1] > 500:
            pygame.draw.rect(screen, bright_green,(650,500,100,60),1)
            screen.blit(Text3, TextRect3)
            if(click[0]==1):
                pygame.quit()
                quit()
        else:
            pygame.draw.rect(screen, red,(650,500,100,60),1)
        
        if 330+145 > mouse[0] > 330 and 500 + 60 > mouse[1] > 500:
            pygame.draw.rect(screen, bright_green,(330,500,145,60),1)
            screen.blit(Text4, TextRect4)
            if(click[0]==1):
                while instructions_state:
                    screen.fill((0,0,0))
                    screen.blit(instructions,(0,0))  
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            instructions_state = False
        else:
            pygame.draw.rect(screen, red,(330,500,145,60),1)
            
        pygame.display.update()
        clock.tick(15)

def simulation():
    pygame.mixer.music.load("mainspace.mp3")
    pygame.mixer.music.play(-1)
    for p in range(500):
        particle_mass = random.randint(1,4)
        particle_size = calculateRadius(particle_mass)
        universe.addParticles(mass=particle_mass, size=particle_size, speed=0)

    key_to_function = {
        pygame.K_LEFT:   (lambda x: x.scroll(dx = 1)),
        pygame.K_RIGHT:  (lambda x: x.scroll(dx = -1)),
        pygame.K_DOWN:   (lambda x: x.scroll(dy = -1)),
        pygame.K_UP:     (lambda x: x.scroll(dy = 1)),
        pygame.K_EQUALS: (lambda x: x.zoom(2)),
        pygame.K_MINUS:  (lambda x: x.zoom(0.5)),
        pygame.K_r:      (lambda x: x.reset())}

    paused = False
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in key_to_function:
                    key_to_function[event.key](universe_screen)
                elif event.key == pygame.K_SPACE:
                    paused = not paused
        if paused:
            pygame.mixer.music.pause()
        if not paused:
            universe.update()
            pygame.mixer.music.unpause()
            
            
        screen.fill(universe.colour)
    
        particles_to_remove = []
        for p in universe.particles:
            if 'collide_with' in p.__dict__:
                particles_to_remove.append(p.collide_with)
                p.size = calculateRadius(p.mass)
                del p.__dict__['collide_with']

            x = int(universe_screen.mx + (universe_screen.dx + p.x) * universe_screen.magnification)
            y = int(universe_screen.my + (universe_screen.dy + p.y) * universe_screen.magnification)
            size = int(p.size * universe_screen.magnification)
            
            if size < 2:
                pygame.draw.rect(screen, p.colour, (x, y, 2, 2))
            else:
                pygame.draw.circle(screen, p.colour, (x, y), size, 0)
    
        for p in particles_to_remove:
            if p in universe.particles:
                universe.particles.remove(p)
        pygame.display.flip()
        clock.tick(80)


intro()
simulation()
pygame.quit()
quit()    
