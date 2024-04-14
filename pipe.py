import pygame
import var


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/pipe.png')
        self.rect = self.image.get_rect()
        # Position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x,y - int(var.pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x,y + int(var.pipe_gap / 2)]

    def update(self):
        self.rect.x -= var.scroll_speed
        if self.rect.right < 0:
            self.kill()