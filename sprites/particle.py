import pygame
import random

class Particle(pygame.sprite.Sprite):
    _surface_cache = {}

    def __init__(self, game, position, color, vector = None, target_position = None):
        self._layer = 8
        super().__init__()
        self.game = game
        self.size = random.randint(2, 5)
        self.life = 255
        
        # 建立一個唯一的標籤 (型號)
        cache_key = (self.size, color)
        
        # 如果倉庫裡還沒刻過這個印章，就現刻一個存起來
        if cache_key not in Particle._surface_cache:
            surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (self.size, self.size), self.size)
            Particle._surface_cache[cache_key] = surf
        
        # 直接拿現成的圖案複本來用，這比重新畫圓快幾百倍
        self.image = Particle._surface_cache[cache_key].copy()
        
        # 設定位置 
        self.position = pygame.math.Vector2(position)
        self.rect = self.image.get_rect(center=position)
        if vector is None:
            self.vector = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        else:
            self.vector = vector

        if target_position:
            self.target_position = target_position
        else:
            self.target_position = None

    def update(self):
        # 位移邏輯
        self.position += self.vector
        self.rect.center = self.position # 更新碰撞盒位置
        
        # 透明度邏輯
        self.life -= 5
        if self.life <= 0:
            self.kill()
        elif self.life % 25 == 0:  # 每降 25 點才重新渲染一次透明度
            self.image.set_alpha(self.life)

        if self.target_position:
            if (self.target_position  - self.position).length() <= 4:
                self.kill()
   
    @staticmethod
    def create_burst(game, position, color, count=10, speed_range=(1, 4)):
        """在指定位置產生一團粒子"""
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(*speed_range)
            vector = pygame.math.Vector2()
            vector.from_polar((speed, angle))
            p = Particle(game, position, color, vector)
            game.all_sprites.add(p)

    @staticmethod
    def create_implosion(game, target_position, color, count = 10, radius = 50, speed_range = (2, 5)):
        """粒子從四周往目標點匯集的蓄力效果"""
        for _ in range(count):
            # 1. 在圓周上隨機找一個起始點
            angle = random.uniform(0, 360)
            offset = pygame.math.Vector2()
            offset.from_polar((radius, angle))
            spawn_pos = pygame.math.Vector2(target_position) + offset
            
            # 2. 計算往目標點移動的向量
            direction = pygame.math.Vector2(target_position) - spawn_pos
            if direction.length() > 0:
                speed = random.uniform(*speed_range)
                vector = direction.normalize() * speed
                
                # 3. 建立粒子 (起始位置是在四周)
                p = Particle(game, spawn_pos, color, vector, target_position)
                game.all_sprites.add(p)
        
    @staticmethod
    def create_explosion(game, position):
        """組合技：炫彩大爆炸"""
        Particle.create_burst(game, position, (255, 255, 255), 10, (1, 4)) # 白色核心
        Particle.create_burst(game, position, (255, 100, 0), 10, (1, 6))   # 橘色火花
        Particle.create_burst(game, position, (255, 255, 0), 10, (1, 4))  # 黃色餘燼