import pygame
import random
import math
from setting import WIDTH, HEIGHT

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, pos, angle):
        self._layer = 4  # 雷射圖層
        super().__init__()
        self.game = game
        self.res = game.res
        self.anim = self.res['anim']['laser']
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.angle = angle

        self.damage = 30
        self.thickness = 20
        self.has_damaged_player = False
        self.pos = pygame.math.Vector2(pos)
        
        # 1. 射線方向
        self.direction = pygame.math.Vector2(0, 1).rotate(-self.angle)
        
        # 2. 決定長度 (給個夠長的值超越螢幕)
        self.length = math.sqrt(WIDTH**2 + HEIGHT**2) 
        
        # 3. 從原圖建立拉長的雷射
        original_img = self.anim[0]
        # 把圖片「拉長」並調整「粗細」(self.thickness)
        stretched_image = pygame.transform.scale(original_img, (self.thickness, int(self.length)))
        
        # 4. 旋轉已經拉長的雷射
        # angle + 180 讓頭部靠近發射點
        self.image = pygame.transform.rotate(stretched_image, self.angle)
        
        # 5. 計算中心點
        # 雷射的起點是 pos + offset，終點是起點 + 方向 * length
        offset = self.direction * 35
        start_pos = self.pos + offset
        end_pos = start_pos + self.direction * self.length
        
        # 實際畫圖的中心點是起點和終點的中間
        center_pos = (start_pos + end_pos) / 2
        self.rect = self.image.get_rect(center=center_pos)
        
        self.mask = pygame.mask.from_surface(self.image)
                
        # 動畫次數計數
        self.play_count = 0 
        self.max_play_count = 1 # 播完 1 次動畫就消失

        self.game.all_sprites.add(self)
        self.game.lasers.add(self) 

    def update(self):
        # 只需要更新動畫，不用移動
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.anim):
                self.frame = 0
                self.play_count += 1
                if self.play_count >= self.max_play_count:
                    self.kill() # 播完指定次數就消失
                    return

            # 拉長並旋轉新的一幀
            original_img = self.anim[self.frame]
            # 這裡也要用 self.thickness 才會保持一樣粗
            stretched_image = pygame.transform.scale(original_img, (self.thickness, int(self.length)))
            self.image = pygame.transform.rotate(stretched_image, self.angle)
            
            # 更新 rect 與 mask
            offset = self.direction * 35
            start_pos = self.pos + offset
            end_pos = start_pos + self.direction * self.length
            center_pos = (start_pos + end_pos) / 2
            
            self.rect = self.image.get_rect(center=center_pos)
            self.mask = pygame.mask.from_surface(self.image)
