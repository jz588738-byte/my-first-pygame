import pygame
import time
import random
from ..power_up import Power_up

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, game, health, score_value, particle_color = (255, 165, 0)):
        self._layer = 3  # 敵機圖層：在隕石上面
        super().__init__()
        self.res = game.res
        self.game = game
        self.game.enemies.add(self)
        self.game.all_sprites.add(self)
        
        self.health = health
        self.score_value = score_value
        self.particle_color = particle_color
        self.image = None
        self.rect = None
        #自身撞到玩家
        self.damage = 60

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game.score += self.score_value
            self.destroy()
        else:
            from sprites.explosion import Explosion
            expl = Explosion(self.game, self.rect.center, 'sm', particle_color = self.particle_color)
            self.game.all_sprites.add(expl)
            self.res['sound']['hit_enemy'].play()

    def destroy(self):
        from sprites.explosion import Explosion
        expl = Explosion(self.game, self.rect.center, 'lg', particle_color = self.particle_color)
        self.game.all_sprites.add(expl)
        self.res['sound']['enemy_death'].play()
        
        if random.random() > 0.9:
            power = Power_up(self.game, self.rect.center)
            self.game.all_sprites.add(power)
            self.game.powers.add(power)
        
        self.kill()


