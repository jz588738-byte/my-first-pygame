import pygame
import random

class Particle(pygame.sprite.Sprite):
    _surface_cache = {}

    def __init__(self, game, position, color, vector=None, target_position=None, life_range=None):
        self._layer = 8
        super().__init__()
        self.game = game
        self.size = random.randint(2, 5)
        self.life = 255
        self.life_time = None
        if life_range:
            self.life_time = random.randint(int(life_range[0] * 1000), int(life_range[1] * 1000))
            self.start_time = pygame.time.get_ticks()
        
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

    def update(self, dt):
        # 位移邏輯
        self.position += self.vector * dt * 60
        self.rect.center = self.position # 更新碰撞盒位置
        if self.life_time is not None:
            if pygame.time.get_ticks() - self.start_time > self.life_time:
                self.kill()
        
        # 透明度邏輯
        self.life -= 5 * dt * 60
        if self.life <= 0:
            self.kill()
        else:
            self.image.set_alpha(max(0, int(self.life)))

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
    def create_implosion(game, target_rect, color, count = 10, radius = 50, speed_range = (2, 5)):
        target_position = target_rect.center
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

    @staticmethod
    def create_fire(game, target_rect, color, count=(3, 5), speed_range=(2, 5)):
        spawn_position = target_rect.top
        count = random.randint(*count)
        for _ in range(count):
            angle = random.uniform(240, 300)
            direction = pygame.math.Vector2()
            direction.from_polar((1, angle))

            if direction.length() > 0:
                speed = random.uniform(*speed_range)
                vector =  direction * speed
                p = Particle(game, target_rect.center, color, vector=vector, life_range=(0.25, 0.5))
                game.all_sprites.add(p)
        
        
