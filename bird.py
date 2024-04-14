import pygame
from const import SCREEN_WIDTH, SCREEN_HEIGHT,DISPLAY_HEIGHT
# from var import ground_scroll, scroll_speed, flying
import var

class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'assets/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if(var.flying == True):
            # Gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < DISPLAY_HEIGHT:
                self.rect.y += int(self.vel)

        if var.game_over == False:
            # Jump
            if (pygame.mouse.get_pressed()[0] == 1) and (self.clicked == False):
                self.clicked = True
                self.vel = -10
            if (pygame.mouse.get_pressed()[0] == 0):
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # Symbolize bird is dead
            self.image = pygame.transform.rotate(self.images[self.index], -90)

