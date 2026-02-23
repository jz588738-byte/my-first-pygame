import pygame.transform

from .base_rock import BaseRock
from setting import *
import random

class SplitRock(BaseRock):
    def __init__(self, res, size = None, center = None):
        super().__init__(res)
        self.size = size if size is not None else 2

        raw_image = self.res['img']['split_rocks'][self.size]

        #定義每一個石頭的大小
        rock_widths = [30, 60, 90]
        target_width = rock_widths[self.size]

        # 保存隨機位置或傳入的中心點
        old_center = center if center else self.rect.center

        self.radius = target_width * 0.85 // 2
        #縮放圖片
        self.image_ori = pygame.transform.scale(raw_image, (target_width, target_width))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.center = old_center # 還原位置


        if center:
            self.rect.center = center

            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-3, 3)

    def split(self, all_sprites, rocks):
        if self.size - 1 >= 0:
            new_size = self.size - 1

            #分裂石頭
            small_rock1 = SplitRock(self.res, new_size, (self.rect.right, self.rect.centery))
            small_rock2 = SplitRock(self.res, new_size, (self.rect.left, self.rect.centery))
            #加入群組
            all_sprites.add(small_rock1, small_rock2)
            rocks.add(small_rock1, small_rock2)
