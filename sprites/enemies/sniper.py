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

    def __init__(self, game : 'Game'):
        super().__init__(game, health = 3, score_value = 100, particle_color = (20, 150, 255))
        self.original_image = self.res['img']['sniper']
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(25, WIDTH - 25), random.randint(-100, -50))
        self.stable_center = pygame.math.Vector2(self.rect.center)
        
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
        self.stable_center.y += 2
        if self.stable_center.y >= self.target_y:
            self.stable_center.y = self.target_y
            self.status = self.STATE_PATROL
        self.rect.center = self.stable_center

    def update_patrol(self):
        self.stable_center.x += self.speed_x * self.direction
        if self.stable_center.x >= WIDTH - self.rect.width // 2:
            self.stable_center.x = WIDTH - self.rect.width // 2
            self.direction = -1 
        elif self.stable_center.x <= self.rect.width // 2:
            self.stable_center.x = self.rect.width // 2
            self.direction = 1
        self.rect.center = self.stable_center
        
        if random.randrange(120) == 0:
            self.status = self.STATE_AIM
            self.aim_start_time = pygame.time.get_ticks()
            # 這個角度用來記錄 Sniper 目前繪製的角度
            self.current_angle = 0
            self.locked_angle = 0
            self.locked_target = None

    def update_aim(self):
        aim_position = self.rect.center
        now = pygame.time.get_ticks()
        elapsed_time = now - self.aim_start_time

        # 0 ~ 1000ms 追蹤玩家，1000ms 之後鎖定最後追蹤的角度與位置
        if elapsed_time < 1000:
            player_position = self.game.player.rect.center
            direction = pygame.math.Vector2(player_position) - self.rect.center
            self.locked_angle = direction.angle_to((0, 1))
            self.locked_target = player_position
        
        # 旋轉圖片
        self.current_angle = self.locked_angle
        self.image = pygame.transform.rotate(self.original_image, self.current_angle)
        self.rect = self.image.get_rect(center = self.stable_center)

        # 蓄力震動與持續粒子效果 (快要發射前的警告)
        if elapsed_time > 1000:
            if not hasattr(self, 'charging_sound_playing') or not self.charging_sound_playing:
                self.res['sound']['charging'].play()
                self.charging_sound_playing = True
            
            # 蓄力震動
            self.rect.center = (self.stable_center.x + random.randint(-2, 2), 
                                self.stable_center.y + random.randint(-2, 2))
            
            # 每 100 毫秒產生一次匯聚粒子
            if not hasattr(self, 'last_charge_particle_time'):
                self.last_charge_particle_time = 0
            
            if now - self.last_charge_particle_time > 100:
                from sprites.particle import Particle
                Particle.create_implosion(self.game, self.rect.center, (215, 30, 70), count=5, radius=60)
                self.last_charge_particle_time = now

        if elapsed_time > 2000:
            if hasattr(self, 'charging_sound_playing') and self.charging_sound_playing:
                self.res['sound']['charging'].fadeout(300)
                self.charging_sound_playing = False
            self.status = self.STATE_FIRE
            self.fire_start_time = now
            self.has_fired = False # 重置發射標記
            self.rect.center = aim_position

    def update_fire(self):
        if not self.has_fired:
            # 依據鎖定的角度產生雷射
            Laser(self.game, self.stable_center, self.locked_angle)
            self.has_fired = True
            self.res['sound']['laser_shoot'].play()

        # 等開火動畫結束 (約 0.6 秒) 回到恢復狀態
        if pygame.time.get_ticks() - self.fire_start_time > 600:
            self.status = self.STATE_RECOVER

    def update_recover(self):
        # current_angle 慢慢向 0 靠攏
        self.current_angle += (0 - self.current_angle) * 0.1 

        center = self.stable_center
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
            direction = pygame.math.Vector2(self.locked_target) - self.stable_center
            if direction.length() > 0:
                direction = direction.normalize()
            
            # 把紅線畫長一點
            end_pos = pygame.math.Vector2(self.stable_center) + direction * 1000
            pygame.draw.line(screen, (255, 0, 0), self.stable_center, end_pos, 2)