import pygame
import time

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, res, game, health, score_value):
        super().__init__()
        self.res = res
        self.game = game
        self.game.enemies.add(self)
        self.game.all_sprites.add(self)
        
        self.health = health
        self.score_value = score_value
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
            expl = Explosion(self.rect.center, 'sm', self.res)
            self.game.all_sprites.add(expl)
            self.res['sound']['hit_enemy'].play()

    def destroy(self):
        from sprites.explosion import Explosion
        expl = Explosion(self.rect.center, 'lg', self.res)
        self.game.all_sprites.add(expl)
        self.res['sound']['enemy_death'].play()
        self.kill()


