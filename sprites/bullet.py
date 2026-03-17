from setting import *
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 6  # 子彈圖層
        super().__init__()
        self.game = game
        self.res = game.res
        self.image = self.res['img']['bullet']
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.pos = pygame.Vector2(self.rect.center)
        self.speedy = -600  # -10 * 60

    def update(self, dt):
        self.pos.y += self.speedy * dt
        self.rect.centery = round(self.pos.y)
        if self.rect.bottom < 0:
            self.kill()
