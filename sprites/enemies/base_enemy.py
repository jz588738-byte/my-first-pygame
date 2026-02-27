import pygame
import time

class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, res, game, health, score_value):
        super().__init__()
        self.res = res
        self.game = game
        self.health = health
        self.score_value = score_value
        self.image = None
        self.rect = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game.score += self.score_value
            self.destroy()

    def destroy(self):
        # 1. 播放爆炸音效 (可選)
        # self.res['sound']['expls'][0].play() 
        
        # 2. 只有在子類別設定了 rect 之後才能在該位置產生爆炸
        if self.rect:
            # 我們直接從 sprites 導入 Explosion (或在呼叫時傳入)
            from sprites.explosion import Explosion
            expl = Explosion(self.rect.center, 'lg', self.res)
            self.game.all_sprites.add(expl)

        # 3. 移除自己
        self.kill()


