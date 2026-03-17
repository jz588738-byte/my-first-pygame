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
        self.speedy = 180  # 3 * 60
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, dt):
        self.pos.y += self.speedy * dt
        self.rect.centery = round(self.pos.y)
        if self.rect.top > HEIGHT:
            self.kill()