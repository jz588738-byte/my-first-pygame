import pygame
import random
from state_machine import State
from setting import *
from ...particle import Particle

class SniperBaseState(State):
    def __init__(self, owner):
        super().__init__(owner)
        self.game = owner.game
        self.res = owner.res

class EntryState(SniperBaseState):
    def enter(self):
        self.owner.status_label = "Entry" # 用於除錯
        self.target_y = random.randint(75, 100)

    def update(self, dt, events=None):
        self.owner.stable_center.y += 2 * dt * 60
        if self.owner.stable_center.y >= self.target_y:
            self.owner.stable_center.y = self.target_y
            self.owner.state_machine.change_state("PatrolState")
        self.owner.rect.center = (round(self.owner.stable_center.x), round(self.owner.stable_center.y))

class PatrolState(SniperBaseState):
    def enter(self):
        self.owner.status_label = "Patrol"

    def update(self, dt, events=None):
        self.owner.stable_center.x += self.owner.speed_x * self.owner.direction * dt * 60
        half_width = self.owner.rect.width // 2
        if self.owner.stable_center.x >= WIDTH - half_width:
            self.owner.stable_center.x = WIDTH - half_width
            self.owner.direction = -1 
        elif self.owner.stable_center.x <= half_width:
            self.owner.stable_center.x = half_width
            self.owner.direction = 1
        self.owner.rect.center = (round(self.owner.stable_center.x), round(self.owner.stable_center.y))
        
        if random.randrange(120) == 0:
            self.owner.state_machine.change_state("AimState")

class AimState(SniperBaseState):
    def enter(self):
        self.owner.status_label = "Aim"
        self.start_time = pygame.time.get_ticks()
        self.owner.locked_target = None
        self.last_charge_particle_time = 0
        self.charging_sound_playing = False

    def update(self, dt, events=None):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        # 1秒內追蹤玩家
        if elapsed < 1000:
            player_pos = self.game.player.rect.center
            direction = pygame.math.Vector2(player_pos) - self.owner.rect.center
            self.owner.locked_angle = direction.angle_to((0, 1))
            self.owner.locked_target = player_pos
            self.owner.image = pygame.transform.rotate(self.owner.original_image, self.owner.current_angle)
            self.owner.rect = self.owner.image.get_rect(center=self.owner.stable_center)
        
        # 旋轉圖片
        self.owner.current_angle = self.owner.locked_angle
        

        # 蓄力效果
        if elapsed > 1000:
            if not self.charging_sound_playing:
                self.res['sound']['charging'].play()
                self.charging_sound_playing = True
            
            # 震動
            self.owner.rect.center = (self.owner.stable_center.x + random.randint(-2, 2), 
                                     self.owner.stable_center.y + random.randint(-2, 2))
            
            # 粒子
            if now - self.last_charge_particle_time > 100:
                Particle.create_implosion(self.game, self.owner.rect, (215, 30, 70), count=5, radius=60)
                self.last_charge_particle_time = now

        if elapsed > 2000:
            self.owner.state_machine.change_state("FireState")

    def exit(self):
        if self.charging_sound_playing:
            self.res['sound']['charging'].fadeout(300)

    def draw(self, screen):
        if self.owner.locked_target:
            direction = pygame.math.Vector2(self.owner.locked_target) - self.owner.stable_center
            if direction.length() > 0:
                direction = direction.normalize()
            end_pos = pygame.math.Vector2(self.owner.stable_center) + direction * 1000
            pygame.draw.line(screen, (255, 0, 0), self.owner.stable_center, end_pos, 2)

class FireState(SniperBaseState):
    def enter(self):
        self.owner.status_label = "Fire"
        self.start_time = pygame.time.get_ticks()
        from ...laser import Laser
        Laser(self.game, self.owner.stable_center, self.owner.locked_angle)
        self.res['sound']['laser_shoot'].play()

    def update(self, dt, events=None):
        if pygame.time.get_ticks() - self.start_time > 600:
            self.owner.state_machine.change_state("RecoverState")

class RecoverState(SniperBaseState):
    def enter(self):
        self.owner.status_label = "Recover"

    def update(self, dt, events=None):
        self.owner.current_angle += (0 - self.owner.current_angle) * 0.1 * dt * 60
        self.owner.image = pygame.transform.rotate(self.owner.original_image, self.owner.current_angle)
        self.owner.rect = self.owner.image.get_rect(center=self.owner.stable_center)

        if abs(self.owner.current_angle) < 1:
            self.owner.current_angle = 0
            self.owner.image = self.owner.original_image.copy()
            self.owner.rect = self.owner.image.get_rect(center=self.owner.stable_center)
            self.owner.state_machine.change_state("PatrolState")
