import pygame
import random
from setting import *
from ..base_enemy import BaseEnemy
from state_machine import StateMachine
from .sniper_states import EntryState

class Sniper(BaseEnemy):
    def __init__(self, game):
        super().__init__(game, health=3, score_value=100, particle_color=(20, 150, 255))
        self.original_image = self.res['img']['sniper']
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(25, WIDTH - 25), random.randint(-100, -50))
        self.stable_center = pygame.math.Vector2(self.rect.center)

        self.damage = 30
        
        self.speed_x = 2
        self.direction = 1
        self.radius = 25
        self.current_angle = 0
        self.locked_angle = 0
        self.locked_target = None
        self.status_label = "" # 僅供除錯或開發人員查看

        # 初始化狀態機
        self.state_machine = StateMachine(self)
        
        from .sniper_states import EntryState, PatrolState, AimState, FireState, RecoverState
        self.state_machine.add_state("EntryState", EntryState(self))
        self.state_machine.add_state("PatrolState", PatrolState(self))
        self.state_machine.add_state("AimState", AimState(self))
        self.state_machine.add_state("FireState", FireState(self))
        self.state_machine.add_state("RecoverState", RecoverState(self))
        
        self.state_machine.change_state("EntryState")

    def update(self, events=None):
        # 委託給狀態機運作
        self.state_machine.update(events)

    def kill(self):
        if self.state_machine.current_state:
            self.state_machine.current_state.exit()
        super().kill()

    def draw_extras(self, screen):
        # 委託給目前狀態畫出額外資訊（例如紅線）
        self.state_machine.draw(screen)
