import pygame
from pygame.locals import *
from const import SCREEN_WIDTH, SCREEN_HEIGHT,DISPLAY_HEIGHT
# from var import ground_scroll, scroll_speed, flying
import var
from bird import Bird
from pipe import Pipe
from button import Button
import utils
import random

# Initialize Pygame
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

var.font = pygame.font.SysFont('Bauhaus 93', 60)

# Load Images
bg = pygame.image.load('assets/bg.png')
ground_img = pygame.image.load('assets/ground.png')
button_img = pygame.image.load('assets/restart.png')

# Groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
# Bird Sprite
flappy = Bird(100, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)
# Button for Restart
button = Button(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2-100, button_img)

run = True
while run:
    clock.tick(fps)
    # Draw Background
    screen.blit(bg, (0,0))

    bird_group.draw(screen)
    bird_group.update()

    pipe_group.draw(screen)

    # Draw and scroll the ground
    screen.blit(ground_img, (var.ground_scroll,DISPLAY_HEIGHT))

    # Check Score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and var.pass_pipe == False:
            var.pass_pipe = True  
        if var.pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                var.score += 1
                var.pass_pipe = False

    # Draw Text
    utils.draw_text( screen, str(var.score), var.font, var.white, int(SCREEN_WIDTH/2),2)

    # Look for collections between sprites / groups
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        var.game_over = True

    # Chek if bird hit the ground
    if flappy.rect.bottom >= DISPLAY_HEIGHT:
        var.game_over = True
        var.flying = False


    if var.game_over == False and var.flying == True:
        # Generate New Pipes
        time_now = pygame.time.get_ticks()
        if (time_now - var.last_pipe) > var.pipe_frequency:
            pipe_height = random.randint(-100,100)
            # Pipe Sprites
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            var.last_pipe = time_now
        # Update Variables
        var.ground_scroll -= var.scroll_speed
        # Reset Scroll
        if abs(var.ground_scroll) > 35:
            var.ground_scroll = 0
        # Only have pipes running when game is still running    
        pipe_group.update()

    # Check for Game Over, and Reset
    if var.game_over == True:
        if button.draw(screen) == True:
            utils.reset_game(pipe_group, flappy, var)
            var.game_over = False           

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.MOUSEBUTTONDOWN and var.flying == False and var.game_over == False:
            var.flying = True
    
    pygame.display.update()

pygame.quit()