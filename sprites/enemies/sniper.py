import pygame
import random
from setting import WIDTH, HEIGHT, BLACK
from .base_enemy import BaseEnemy
from ..laser import Laser

# --- 2. 狙擊手本體類別 ---
class Sniper(BaseEnemy):
    
    STATE_ENTRY = 'entry'
    STATE_PATROL = 'patrol'
    STATE_AIM = 'aim'
    STATE_FIRE = 'fire'
    STATE_RECOVER = 'recover'

    def __init__(self, res : dict, game : 'Game'):
        super().__init__(res, game, health = 3, score_value = 100)
       
        self.original_image = self.res['img']['sniper']
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(25, WIDTH - 25), random.randint(-100, -50))
        
        self.status = self.STATE_ENTRY
        self.target_y = random.randint(50, 100)

        self.speed_x = 2
        self.direction = 1
        self.has_fired = False
        
        self.radius = 25 # 增加半徑用於碰撞

    def update(self):
        # 狀態總管
        if self.status == self.STATE_ENTRY:
            self.update_entry()
        elif self.status == self.STATE_PATROL:
            self.update_patrol()
        elif self.status == self.STATE_AIM:
            self.update_aim()
        elif self.status == self.STATE_FIRE:
            self.update_fire()
        elif self.status == self.STATE_RECOVER:
            self.update_recover()

    def update_entry(self):
        self.rect.y += 2
        if self.rect.centery >= self.target_y:
            self.rect.centery = self.target_y
            self.status = self.STATE_PATROL

    def update_patrol(self):
        self.rect.x += self.speed_x * self.direction
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.direction = -1 
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
        
        if random.randrange(120) == 0:
            self.status = self.STATE_AIM
            self.aim_start_time = pygame.time.get_ticks()
            # 這個角度用來記錄 Sniper 目前繪製的角度
            self.current_angle = 0
            self.locked_angle = 0
            self.locked_target = None

    def update_aim(self):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.aim_start_time

        # 0 ~ 1000ms 追蹤玩家，1000ms 之後鎖定最後追蹤的角度與位置
        if elapsed_time < 1000:
            player_position = self.game.player.rect.center
            direction = pygame.math.Vector2(player_position) - self.rect.center
            self.locked_angle = direction.angle_to((0, 1))
            self.locked_target = player_position
        
        # 旋轉圖片
        center = self.rect.center
        self.current_angle = self.locked_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center = center)

        # 蓄力震動 (快要發射前的警告)
        if elapsed_time > 1500:
            self.rect.center = (center[0] + random.randint(-2, 2), 
                                center[1] + random.randint(-2, 2))

        if elapsed_time > 2000:
            self.status = self.STATE_FIRE
            self.fire_start_time = now

    def update_fire(self):
        if not self.has_fired:
            # 依據鎖定的角度產生雷射
            Laser(self.res, self.game, self.rect.center, self.locked_angle)
            self.has_fired = True
            self.res['sound']['laser_shoot'].play()

        # 等開火動畫結束 (約 0.6 秒) 回到恢復狀態
        if pygame.time.get_ticks() - self.fire_start_time > 600:
            self.status = self.STATE_RECOVER

    def update_recover(self):
        # 使用 lerp (線性插值) 平滑轉回 0 度
        # current_angle 慢慢向 0 靠攏
        self.current_angle += (0 - self.current_angle) * 0.1 

        center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center = center)

        # 當角度夠接近 0 的時候，就完全回到巡邏狀態
        if abs(self.current_angle) < 1:
            self.current_angle = 0
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center = center)
            self.status = self.STATE_PATROL
            self.has_fired = False

    def draw_extras(self, screen):
        # 只有在瞄準狀態下才畫紅線
        if self.status == self.STATE_AIM and self.locked_target:
            # 算出指向玩家的方向並標準化
            direction = pygame.math.Vector2(self.locked_target) - self.rect.center
            if direction.length() > 0:
                direction = direction.normalize()
            
            # 把紅線畫長一點（例如 1000 像素，足以貫穿畫面）
            end_pos = self.rect.center + direction * 1000
            pygame.draw.line(screen, (255, 0, 0), self.rect.center, end_pos, 2)