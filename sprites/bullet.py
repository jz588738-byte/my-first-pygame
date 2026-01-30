from setting import *
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, res):
        super().__init__()
        self.res = res
        self.image = self.res['img']['bullet']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
