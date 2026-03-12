import pygame
from setting import * 
from .base_rock import BaseRock
from ..power_up import Power_up
import random

class ExplodingRock(BaseRock):

    def __init__(self, game : 'Game'):
        super().__init__(game)
        self.is_exploding = False
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 50

        
        raw_image = random.choice(self.res['img']['exploding_rock'])
        
        rock_width = [100, 120, 140]
        self.target_width = random.choice(rock_width)
        
        self.radius = self.target_width * 0.85// 2
        self.damage = self.radius

        # 保存父類別 BaseRock 產生的隨機位置
        old_center = self.rect.center
        
        self.image_ori = pygame.transform.scale(raw_image, (self.target_width, self.target_width))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.center = old_center # 還原隨機位置

        # 效能優化：預先縮放爆炸後的每一幀動畫，避免在 update 迴圈中使用極耗能的 scale 函數
        self.expl_images = []
        for img in self.res['anim']['damage_exploding']:
            self.expl_images.append(pygame.transform.scale(img, (self.target_width, self.target_width)))
    
    def destroy(self, game, Explosion):
        self.kill() # 從所有群組移除 (包含 rocks)
        game.all_sprites.add(self) # 加回 all_sprites 確保 update/draw 正常
        self.is_exploding = True
        self.res['sound']['damage_exploding'].play()

        if random.random() > 0.9:
            power = Power_up(game, self.rect.center)
            game.all_sprites.add(power)
            game.powers.add(power)

        game.score += int(self.radius)

        
        from .split_rock import SplitRock  # 在函式內導入以避免循環引用
        
        for rock in game.rocks:
            # 排除自己，且排除已經在爆炸中的隕石（避免重複觸發無限連鎖）
            if rock != self and not (isinstance(rock, ExplodingRock) and rock.is_exploding):
                # 計算距離
                dist_sq = (self.rect.centerx - rock.rect.centerx) ** 2 + (self.rect.centery - rock.rect.centery) ** 2
                explosion_radius = self.radius * 2.5
                
                if dist_sq < explosion_radius ** 2:
                    # 連鎖摧毀！
                    rock.destroy(game, Explosion)
        
        from sprites.particle import Particle
        Particle.create_explosion(game, self.rect.center)
        # 使用預先縮放好的圖片
        self.image = self.expl_images[self.frame]
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.is_exploding:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_duration:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.expl_images):
                    self.kill()
                else:
                    # 使用預先縮放好的圖片，速度提升 10 倍以上
                    self.image = self.expl_images[self.frame]
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
        else:
            super().update()