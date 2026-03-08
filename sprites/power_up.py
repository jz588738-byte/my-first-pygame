import pygame
from setting import *
import random

class Power_up(pygame.sprite.Sprite):
    def __init__(self, game, center):
        self._layer = 2  # 寶物圖層：在隕石上面
        super().__init__()
        self.game = game
        self.res = game.res
        self.type = random.choice(list(self.res['power_up_img'].keys()))
        self.image = self.res['power_up_img'][self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()