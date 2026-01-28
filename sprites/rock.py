from setting import *
import pygame
import random

class Rock(pygame.sprite.Sprite):
    def __init__(self,rocks_img):
        super().__init__()
        self.image_ori = random.choice(rocks_img)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 // 2
        #初始位置
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200,-100)
        self.speedy = random.randrange(2,5)
        self.speedx = random.randrange(-1,1)
        self.total_degree = 0
        self.rot_degree = random.randrange(-2, 2)

    #石頭旋轉
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-1,1)