#TODO
#add dash (200 pixels in one direction, 1.5s cooldown)
#add hp
#add stats (defense (x% reduction in damage))
#add enemies (melee (basic, dasher), ranged(bow, blaster))
#add attacks
#add player sprite
#add weapons (stick, sword(s), crossbow, gun(single-shot, auto), utility (passive stat increase))
#add currency (gain from kills, start with zero)
#add shop (3 items, random items and 2 utility items (new one spawns when anything is bought))
#add secret fight
#/TODO

#this is absolutely turning into a roguelike/roguelite lmaooo

#NOTE
#pygame.transform.scale can make a surface bigger
#i.e. image = pygame.transform.scale(image,
#                                   (image.get_width() * 2,
#                                    image.getheight() * 2))
#reversed vectors (+X = left, +y = down)
#with PNGs you can use convert_alpha() to get rid of black pixels
#.set_colorkey to ignore a colour i.e. greenscreening = image.set_colorkey((0,255,0))
#blank surfaces = pygame.Surface((x,y), pygame.SRCALPHA)
#/NOTE

import pygame
from pygame.locals import *
import sys
pygame.init()
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
#im not sure why i cant just write 1600 and 900 in the screen and background variables but i trust codingwithruss


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background=pygame.image.load('BHBackgroundtest.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

delta_time = 0.1
x=0

player = pygame.Rect(800, 450, 50, 50)
font = pygame.font.Font(None, size=30)
HP = 100 #unused atm

running = True
while running:
    #need main menu here

    #menu end
    screen.blit(background, (0, 0))
    def fps_counter():
        fps = str(int(clock.get_fps()))
        fps_t = font.render(fps , 1, pygame.Color("YELLOW"))
        screen.blit(fps_t,(0,0))
    fps_counter()


    clock.tick(240) # i have 240hz so it works

    pygame.draw.rect(screen, (255, 255, 255), player)
    x += 50 * delta_time

    key =pygame.key.get_pressed()
    if key [pygame.K_a] == True:
        player.move_ip(-10,0)
    if key [pygame.K_d] == True:
        player.move_ip(10,0)
    if key [pygame.K_w] == True:
        player.move_ip(0,-10)
    if key [pygame.K_s] == True:
        player.move_ip(0,10)




    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, 0.1, delta_time)

pygame.quit()
sys.exit()
