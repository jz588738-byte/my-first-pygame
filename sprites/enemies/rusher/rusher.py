from setting import HEIGHT
import random
import pygame
from ..base_enemy import BaseEnemy
from setting import *
from state_machine import StateMachine
from .rusher_states import EntryState, WarningState, BurstState

class Rusher(BaseEnemy):
    def __init__(self, game, spawn_x):
        super().__init__(game, health=5, score_value=150, particle_color=(65, 65, 75))
        self.image = self.res['img']['rusher']
        self.rect = self.image.get_rect()

        self.rect.centerx = spawn_x
        self.rect.bottom = 0
        self.pos = pygame.Vector2(self.rect.center)
        self.damage = 40
        self.speed_y = 8
        self.burst_speed_y = 12
        self.has_boosted = False
        
        self.state_machine = StateMachine(self)
        self.state_machine.add_state('EntryState', EntryState(self))
        self.state_machine.add_state('WarningState', WarningState(self))
        self.state_machine.add_state('BurstState', BurstState(self))
        
        self.state_machine.change_state('EntryState')
    
    def update(self, dt, events=None):
        self.state_machine.update(dt, events)

    def draw_extras(self, screen):
        self.state_machine.draw(screen)

    @staticmethod
    def create_rusher(game):
        center_x_list = []
        count = random.randint(1, 5)
        spawn_x_range_list = [[0, 550]]
        for _ in range(count):
            #挑選目標生成區間
            target_x_range = random.choice(spawn_x_range_list)
            position_x = random.randint(*target_x_range)
            center_x_list.append(position_x + 25)
            spawn_x_range_list.remove(target_x_range)
            #判斷左、右邊是否還有足夠空間生成
            left_range = [target_x_range[0], position_x - 50]
            right_range = [position_x + 50, target_x_range[1]]
            if left_range[1] >= left_range[0]:
                spawn_x_range_list.append(left_range)
            if right_range[1] >= right_range[0]:
                spawn_x_range_list.append(right_range)
        
        for center_x in center_x_list:
            Rusher(game, center_x)
            
                