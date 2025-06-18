import pygame

pygame.init()
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900




screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background=pygame.image.load('BHBackgroundtest.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()



player = pygame.Rect(800, 450, 50, 50)
speed = 10 # 10 pixels/second

stillplaying = True
while stillplaying:
    screen.blit(background, (0, 0))
    dt = clock.tick(240) / 1000 # 240fps



    pygame.draw.rect(screen, (255, 255, 255), player)
    # SOCD intended
    keys = pygame.key.get_pressed()
    dx = dy = 0
    if keys[pygame.K_a]:
        dx = -speed
    if keys[pygame.K_d]:
        dx = speed
    if keys[pygame.K_w]:
        dy = -speed
    if keys[pygame.K_s]:
        dy = speed
    


    new_x = player.x + dx
    new_y = player.y + dy


    if new_x < 0:
        new_x = 0
    elif new_x + player.width > SCREEN_WIDTH:
        new_x = SCREEN_WIDTH - player.width


    if new_y < 0:
        new_y = 0
    elif new_y + player.height > SCREEN_HEIGHT:
        new_y = SCREEN_HEIGHT - player.height

 
    player.x = new_x
    player.y = new_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stillplaying = False

    pygame.display.flip()

pygame.quit()
