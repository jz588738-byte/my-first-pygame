from setting import HEIGHT
import pygame
from state_machine import State
from setting import *
import random
from ...particle import Particle

class RusherBaseState(State):
    def __init__(self, owner):
        super().__init__(owner)
        self.game = owner.game
        self.res = owner.res

class EntryState(RusherBaseState):
    def enter(self):
        self.owner.state_label = 'Entry'

    def update(self, dt, events=None):
        self.owner.pos.y += self.owner.speed_y * dt * 60
        if self.owner.pos.y >= self.owner.rect.height / 2:
            self.owner.pos.y = self.owner.rect.height / 2
            self.owner.state_machine.change_state('WarningState')
        self.owner.rect.centery = self.owner.pos.y

class WarningState(RusherBaseState):
    def enter(self):
        self.owner.state_label = 'Warning'
        self.start_time = pygame.time.get_ticks()

    def update(self, dt, events=None):
        now = pygame.time.get_ticks()
        if now - self.start_time >= 1000:
            self.owner.state_machine.change_state('BurstState')

    def draw(self, screen):
        end_pos = (self.owner.rect.centerx, HEIGHT)
        pygame.draw.line(screen, (165, 95, 25), self.owner.rect.center, end_pos, 2)


class BurstState(RusherBaseState):
    def enter(self):
        self.owner.state_label = 'Burst'
        self.start_time = pygame.time.get_ticks()
        self.owner.image = self.game.res['img']['rusher_go']
    
    def update(self, dt, events=None):
        now = pygame.time.get_ticks()
        #查看玩家是否有經過rusher的方向
        if abs(self.owner.rect.centerx - self.game.player.rect.centerx) < 50:
            self.owner.has_boosted = True
            self.owner.image = self.game.res['img']['rusher_burst']
            
        
        if now - self.start_time >= 1000:
            if self.owner.has_boosted:
                self.owner.pos.y += self.owner.burst_speed_y * dt * 60
            else:
                self.owner.pos.y += self.owner.speed_y * dt * 60
            self.owner.rect.centery = self.owner.pos.y
        
        if self.owner.rect.top >= HEIGHT:
            self.owner.kill()
    
    def draw(self, screen):
        if self.owner.has_boosted:
            Particle.create_fire(self.game, self.owner.rect, (105, 5, 140))
        else:
            Particle.create_fire(self.game, self.owner.rect, (10, 25, 130))