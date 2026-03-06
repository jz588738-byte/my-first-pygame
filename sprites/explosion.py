import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center, size, particle_color = (255, 165, 0)):
        super().__init__()
        self.game = game
        self.res = game.res
        self.size = size
        self.image = self.res['anim'][size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
        # 產生碎片粒子
        from .particle import Particle
        if self.size == 'player_die':
            Particle.create_explosion(self.game, center)
        else:
            Particle.create_burst(self.game, center, particle_color)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.res['anim'][self.size]):
                self.kill()
            else:
                self.image = self.res['anim'][self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center