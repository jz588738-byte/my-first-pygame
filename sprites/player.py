from setting import *
import pygame
from .bullet import Bullet
import math
import time

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
        self.lives = 3
        self.health = 100
        self.is_respawn = False
        self.is_invincibility = False
        self.respawn_time = 0
        #自動射擊/射速
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #復活多久可以動
        if self.is_respawn and pygame.time.get_ticks() - self.respawn_time > 1000:
            self.is_respawn = False
            self.rect.centerx = WIDTH // 2
            self.rect.bottom = HEIGHT - 10
        #鍵盤控制邏輯
        if not self.is_respawn:
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
        if now - self.last_shot > self.shoot_delay and not self.is_respawn:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top, self.res)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.res['sound']['shoot'].play()

    def respawn(self):
        self.is_respawn = True
        self.is_invincibility = True
        self.respawn_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH // 2, HEIGHT + 500)

    # def invincibility(self):
    #     speed = 10
    #     current_time = time.time()
    #     #利用sin函數讓閃光變平滑
    #     sin_value = math.sin(current_time * speed)
    #     #用sin值控制透明度
    #     alpha = (sin_value + 1) / 2 * 255
    #     self.image.set_alpha(int(alpha))
