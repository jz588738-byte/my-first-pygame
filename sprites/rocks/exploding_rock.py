import pygame
from setting import * 
from .base_rock import BaseRock
import random

class ExplodingRock(BaseRock):

    def __init__(self, res):
        super().__init__(res)
        self.res = res
        
        self.is_exploding = False
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_duration = 50

        
        raw_image = random.choice(self.res['img']['exploding_rock'])
        
        rock_width = [100, 120, 140]
        self.target_width = random.choice(rock_width)
        
        self.radius = self.target_width * 0.85// 2

        # 保存父類別 BaseRock 產生的隨機位置
        old_center = self.rect.center
        
        self.image_ori = pygame.transform.scale(raw_image, (self.target_width, self.target_width))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.center = old_center # 還原隨機位置
    
    def damage_exploding(self, all_sprites, rocks, Explosion, game):
        all_sprites.add(self)
        self.is_exploding = True
        self.res['sound']['damage_exploding'].play()
        
        # 爆炸範圍邏輯：摧毀範圍內的隕石
        from .split_rock import SplitRock  # 在函式內導入以避免循環引用
        
        for rock in rocks:
            # 排除自己，且排除已經在爆炸中的隕石（避免重複觸發無限連鎖）
            if rock != self and not (isinstance(rock, ExplodingRock) and rock.is_exploding):
                # 計算距離
                dist_sq = (self.rect.centerx - rock.rect.centerx) ** 2 + (self.rect.centery - rock.rect.centery) ** 2
                explosion_radius = self.radius * 2.5
                
                if dist_sq < explosion_radius ** 2:
                    # 每炸掉一個隕石就加分
                    game.score += int(rock.radius)
                    
                    # 判斷被炸到的隕石類型，觸發各自的死亡效果
                    if isinstance(rock, ExplodingRock):
                        # 連鎖反應！
                        rock.damage_exploding(all_sprites, rocks, Explosion, game)
                    else:
                        if isinstance(rock, SplitRock):
                            rock.split(all_sprites, rocks)
                        
                        # 為普通隕石或分裂前的大隕石產生爆炸動畫
                        expl = Explosion(rock.rect.center, 'lg', self.res)
                        all_sprites.add(expl)
                        rock.kill() # 摧毀隕石
        
        exploding_image = self.res['anim']['damage_exploding'][self.frame] 
        self.image = pygame.transform.scale(exploding_image, (self.target_width, self.target_width))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        if self.is_exploding:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_duration:
                self.last_update = now
                self.frame += 1
                if self.frame == len(self.res['anim']['damage_exploding']):
                    self.kill()
                else:
                    exploding_image = self.res['anim']['damage_exploding'][self.frame]
                    self.image = pygame.transform.scale(exploding_image, (self.target_width, self.target_width))
                    center = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = center
        else:
            super().update()