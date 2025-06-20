#TODO
#add dash (200 pixels in one direction, 1.5s cooldown)

#add enemies (melee (basic, dasher), ranged(bow, blaster))
#add attacks

#add weapons (stick, sword(s), crossbow, gun(single-shot, auto), utility (passive stat increase))
#add currency (gain from kills, start with zero)
#add shop (3 items, random items and 2 utility items (new one spawns when anything is bought))
#add secret fight
#/TODO

#NOTE
#reversed vectors (+X = left, +y = down) (i hate this rule)
#.set_colorkey to ignore a colour i.e. greenscreening = image.set_colorkey((0,255,0))
#blank surfaces = pygame.Surface((x,y), pygame.SRCALPHA) 
#/NOTE

import pygame
from pygame.locals import *
import sys
import os
import button
import random
import math
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

os.chdir('C:/Users/david/Documents/projects!!/roguelike experiment')
        
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Roguelike Experiment')


titlebackground = pygame.image.load('background/titlescreenBG.png')
titlebackground = pygame.transform.scale(titlebackground, (SCREEN_WIDTH, SCREEN_HEIGHT))


start = pygame.image.load("button/STARTbutton.png")
exit = pygame.image.load("button/EXITbutton.png")
options = pygame.image.load("button/OPTIONSbutton.png")
Continue = pygame.image.load("button/CONTINUEbutton.png")
menu = pygame.image.load("button/MENUbutton.png")
restart = pygame.image.load("button/RESTARTbutton.png")


#player spritesheet test
PlayerSpritesheet = pygame.image.load('sprites/Player/spritesheet.png')
def get_image(spritesheet, width, height, x, y):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(spritesheet, (0,0), (x, y, width, height))
    return image

facingDown = get_image(PlayerSpritesheet, 13, 25, 0, 0)
facingUp = get_image(PlayerSpritesheet, 13, 25, 13, 0)
facingLeft = get_image(PlayerSpritesheet, 13, 25, 26, 0)
facingRight = get_image(PlayerSpritesheet, 13, 25, 0, 25)
#load bad guys
DummyIMG = pygame.image.load('sprites/Enemy/Dummy.png')
#load you

#fonts here

fpsfont = pygame.font.Font(None, size=30)
statfont = pygame.font.Font('font/Stepalange.otf', size=50)
deathfont = pygame.font.Font('font/Stepalange.otf', size=100)
titlefont =pygame.font.Font('font/Stepalange.otf', size=75)
creditfont = pygame.font.Font('font/StepalangeShort.otf', size=30)
#button instances


Menu = True
PauseMenu = False
optionsMenu = False
x=0
y=0




delta_time = 0.1

clock = pygame.time.Clock()
clock.tick(240)


#stats
STRENGTH = 0 # +1 strength = +1 melee damage
DEFENSE = 0 # +1 defense = +1% damage reduction
RANGED = 0 # +1 ranged + +1 ranged damage
SPEED = 5 # +1 walkspeed = +1 pixel/second


#sprite layer groups
projectilesprite = pygame.sprite.Group()


#Dummy class
class Dummy(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, scale, HP):
        super().__init__()
        #def img
        self.sprite = DummyIMG
        width= sprite.get_width()
        height = sprite.get_height()
        self.sprite = pygame.transform.scale(sprite, (int(width*scale), int(height*scale)))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = (x,y)
        self.HP = math.inf
    def draw(self):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))

#Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, scale, playerHP):
        super().__init__()
        self.scale = scale
        self.playerHP = playerHP
        self.direction = "down" 
        self.sprites = {
            "down": self.scale_image(sprite),
            
        }
        self.sprite = self.sprites["down"]
        self.rect = self.sprite.get_rect(topleft=(x, y))
    
    def scale_image(self, image):
        width = image.get_width()
        height = image.get_height()
        return pygame.transform.scale(image, (int(width * self.scale), int(height * self.scale)))

    def add_direction_sprite(self, direction_name, image):
        self.sprites[direction_name] = self.scale_image(image)

    def change_direction(self, new_direction):
        if new_direction != self.direction:
            self.direction = new_direction
            self.sprite = self.sprites[new_direction]
            pos = self.rect.topleft
            self.rect = self.sprite.get_rect(topleft=pos)

    def draw(self):
        screen.blit(self.sprite, self.rect.topleft)

player = Player((610), (600), facingDown, 4, 100)
player.add_direction_sprite("up", facingUp)
player.add_direction_sprite("left", facingLeft)
player.add_direction_sprite("right", facingRight)

playerIMG = player.sprite
#enemy instances       
dummyENT = Dummy((610), (150), DummyIMG, 4, math.inf,)


GetAttacked = False
MeleeAttackedEnemy = False
RangeAttackedEnemy = False
KilledEnemy = False
Gold = 0
Weapon1 = "Stick"
Weapon2 = "None"
Weapon3 = "None"


EnemyAttackDMG = 1

def showtitlescreen():
    titlescreen1 = str("ROGUELIKE")
    rendertitlescreen = titlefont.render(titlescreen1, 1, pygame.Color("WHITE"))
    screen.blit(rendertitlescreen, (500, 30))
    titlescreen2 = str("e x p e r i m e n t")
    rendertitlescreen2 = titlefont.render(titlescreen2, 1, pygame.Color("WHITE"))
    screen.blit(rendertitlescreen2, (410, 100))
    credit = str("created by cyclxne!")
    rendercredit = creditfont.render(credit, 1, pygame.Color("WHITE"))
    creditPFP = pygame.image.load('cyclxne.png').convert_alpha()
    creditbutton = button.Button(760, 640, creditPFP, 0.1)
    creditbutton.draw(screen)
    screen.blit(rendercredit, (535, 650))

#unused button need it for pause menu pls ignore
# continue_button = button.Button(x, y, Continue, 0.5)



start_button = button.Button(540, 200, start, 0.5)
exit_button = button.Button(540, 500, exit, 0.5)
options_button = button.Button(540, 350, options, 0.5)
restart_button = button.Button(530, 420, restart, 0.5)
menu_button = button.Button(530, 430, menu, 0.5)

#loop
running = True
while running:
    #need main menu here
    if Menu == True:
        

        start_clicked = start_button.draw(screen)
        exit_clicked = exit_button.draw(screen)
        options_clicked = options_button.draw(screen)

        player.playerHP = 100
        screen.blit(titlebackground, (0,0))

        start_button.active = True
        exit_button.active = True
        options_button.active = True
        menu_button.active = False

        start_button.draw(screen)
        exit_button.draw(screen)
        options_button.draw(screen)
        showtitlescreen()
    #button actions
        if start_clicked:
            Menu = False
            start_button.active = False
            exit_button.active = False
            options_button.active = False
            
        if exit_clicked:
            running = False

        if options_clicked:
            Menu = False
            optionsMenu = True

            options_button.active = False
            start_button.active = False
            exit_button.active = False
            menu_button.active = True

    if optionsMenu == True:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # RGBA with alpha
        screen.blit(titlebackground, (0, 0))
        screen.blit(overlay, (0, 0))

        optionText = "OPTIONS"
        
        optionText_t = titlefont.render(optionText, 1, pygame.Color("WHITE"))
        optionText_rect = optionText_t.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(optionText_t, optionText_rect)

        optionText1 = "Nothing here yet..."
        optionText1_t = statfont.render(optionText1, 1, pygame.Color("WHITE"))
        optionText1_rect = optionText1_t.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT//2 - 100))
        screen.blit(optionText1_t, optionText1_rect)    
    if menu_button.active:
        if menu_button.draw(screen):
            Menu = True
            optionsMenu = False

            start_button.active = True
            exit_button.active = True
            options_button.active = True
            menu_button.active = False
    if Menu == False and not optionsMenu:

        background = pygame.image.load("background/TUTORIAL_BG.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))
        def fps_counter():
            fps = str(int(clock.get_fps()))
            fps_t = fpsfont.render(fps , 1, pygame.Color("YELLOW"))
            screen.blit(fps_t,(0,0))

        def stat_counter():
            HPrender = str(player.playerHP)
            HP_t = statfont.render("HP: "+HPrender, 1, pygame.Color("WHITE"))
            screen.blit(HP_t, (0,680))
            STRrender = str(STRENGTH)
            STR_t = statfont.render("STR: "+STRrender, 1, pygame.Color("red"))
            screen.blit(STR_t, (0,480))
            DEFrender = str(DEFENSE)
            def_t = statfont.render("DEF: "+DEFrender, 1, pygame.Color("DODGERBLUE"))
            screen.blit(def_t, (0,580))
            RANGErender = str(RANGED)
            RANGE_t = statfont.render("RANGE: "+RANGErender, 1, pygame.Color("darkorange"))
            screen.blit(RANGE_t, (0,530))
            SPDrender = str(SPEED)
            SPD_t = statfont.render("SPEED: "+SPDrender, 1, pygame.Color("LIME"))
            screen.blit(SPD_t, (0, 630))
            MoneyRender = str(Gold)
            Money_t = statfont.render(MoneyRender+" Gold", 1, pygame.Color("GOLD"))
            screen.blit(Money_t, (SCREEN_WIDTH -120, 20))

        
        if Weapon1 == "Stick":
            MeleeDMG = 1
            RangedDMG = 0

        def game_over():
            global Menu

            gameover = str("You died.")
            rendergameover =deathfont.render(gameover, 1, pygame.Color("RED"))
            rect = rendergameover.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
            screen.fill((0,0,0))
            screen.blit(rendergameover, rect)
            #restart button
            restart_button = button.Button(530, 420, restart, 0.5)
            if restart_button.draw(screen):
                Menu = False
                player.playerHP = 100
                player.rect.topleft = (610, 600)
                player.change_direction("down")
            #main menu button
            menu_button = button.Button(530, 500, menu, 0.5)
            if menu_button.draw(screen):
                Menu = True

        
        #getting attacked
        if GetAttacked == True:
            player.playerHP -= EnemyAttackDMG * (DEFENSE/100)
            GetAttacked = False
        #attacking something
        if MeleeAttackedEnemy:
            Damage = MeleeDMG + STRENGTH
        if RangeAttackedEnemy:
            Damage = RangedDMG + RANGED


           
        
        dummyENT.draw()
        player.draw()
        stat_counter() 
        fps_counter()
        if player.rect.colliderect(dummyENT):
            print("colliding") # until i fix movement and collisions

        #consistent movement across fps drops
        x += 50 * delta_time
        #cant move if dead, will use for death animation later on
        if player.playerHP > 0:
            key =pygame.key.get_pressed()
            
            if key [pygame.K_w] or key [pygame.K_UP]:
                player.rect.move_ip(0,-SPEED)
                player.change_direction("up")
            if key [pygame.K_s] or key [pygame.K_DOWN]:            
                player.rect.move_ip(0,SPEED)
                player.change_direction("down")
            if key [pygame.K_a] or key [pygame.K_LEFT]:
                player.rect.move_ip(-SPEED,0)
                player.change_direction("left")
            if key [pygame.K_d] or key [pygame.K_RIGHT]:
                player.rect.move_ip(SPEED,0)
                player.change_direction("right")
            if key[pygame.K_ESCAPE]:
                PauseMenu = True
            if key[pygame.K_y]:
                player.playerHP = 0
        else:
            game_over()

        if PauseMenu == True:
            print("pausing! oh no... fail")

    

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.flip()
    delta_time = clock.tick(240) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

    
pygame.quit()
sys.exit()
