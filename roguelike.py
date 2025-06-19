#TODO
#add dash (200 pixels in one direction, 1.5s cooldown)

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
import button
import random
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Roguelike Experiment')
#images
background=pygame.image.load('RogueBackgroundGRASS.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
start = pygame.image.load('STARTbutton.png').convert_alpha()
exit = pygame.image.load('EXITbutton.png').convert_alpha()

clock = pygame.time.Clock()


#button instances

start_button = button.Button(540, 250, start, 0.5)
exit_button = button.Button(540, 400, exit, 0.5)

Menu = True

x=0
y=0
HP = 100
delta_time = 0.1
#create him
player = pygame.Rect(610, 650, 50, 50)

#fonts here
fpsfont = pygame.font.Font(None, size=30)
statfont = pygame.font.Font(None, size=50)
deathfont = pygame.font.Font(None, size=100)

#stats
STRENGTH = 0 # +1 strength = +1 melee damage
DEFENSE = 0 # +1 defense = +1% damage reduction
RANGED = 0 # +1 ranged + +1 ranged damage
SPEED = 10 # +1 walkspeed = +1 pixel/second

GetAttacked = False
MeleeAttackedEnemy = False
RangeAttackedEnemy = False

Weapon = "Stick"




EnemyAttackDMG = 1
#loop
running = True
while running:
    #need main menu here
    if Menu == True:
        screen.fill((52, 52, 52))

    if start_button.draw(screen):
        Menu = False
        screen.blit(background, (0, 0))
    
    if exit_button.draw(screen):
        running = False

    if Menu == False:
        start_button = button.Button(0, 0, start, 0)
        exit_button = button.Button(0, 0, exit, 0)
    #menu end
    if Menu == False:
        screen.blit(background, (0, 0))
    def fps_counter():
        fps = str(int(clock.get_fps()))
        fps_t = fpsfont.render(fps , 1, pygame.Color("YELLOW"))
        screen.blit(fps_t,(0,0))
    
    fps_counter()

    def HP_counter():
        HPrender = str(HP)
        HP_t = statfont.render("HP: "+HPrender, 1, pygame.Color("RED"))
        screen.blit(HP_t, (0,850))
    if Menu == False:
        HP_counter()

    
    if Weapon == "Stick":
        MeleeDMG = 1
        RangedDMG = 0
    clock.tick(240) # i have 240hz so it works

    def game_over():
        gameover = str("You died.")
        rendergameover =deathfont.render(gameover, 1, pygame.Color("RED"))
        rect = rendergameover.get_rect(center=(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
        screen.fill((0,0,0))
        screen.blit(rendergameover, rect)
        
    
    #getting attacked
    if GetAttacked == True:
        HP -= EnemyAttackDMG * (DEFENSE/100)
        GetAttacked = False
    #attacking something
    if MeleeAttackedEnemy:
        Damage = MeleeDMG + STRENGTH
    if RangeAttackedEnemy:
        Damage = RangedDMG + RANGED


    if Menu == False:
        pygame.draw.rect(screen, (255, 255, 255), player)
    #consistent movement across fps drops
    x += 50 * delta_time
    #cant move if dead, will use for death animation later on
    if HP > 0:
        key =pygame.key.get_pressed()

        if key [pygame.K_w] or key [pygame.K_UP]:
            player.move_ip(0,-SPEED)
        if key [pygame.K_a] or key [pygame.K_LEFT]:
            player.move_ip(-SPEED,0)
        if key [pygame.K_s] or key [pygame.K_DOWN]:            
            player.move_ip(0,SPEED)
        if key [pygame.K_d] or key [pygame.K_RIGHT]:
            player.move_ip(SPEED,0)
        

        #gameover testing
        if key [pygame.K_ESCAPE] == True:
            HP = -1
            HPrender = HP
    else:
        game_over()
    


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, 0.1, delta_time)
    
pygame.quit()
sys.exit()
