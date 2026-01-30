from setting import *
import pygame
from .bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, res ):
        super().__init__()
        self.res = res
        self.image = pygame.transform.scale(self.res['img']['player'],(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        #自動射擊/射速
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #鍵盤控制邏輯
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        #邊界控制
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, bullets):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, self.res)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.res['sound']['shoot'].play()