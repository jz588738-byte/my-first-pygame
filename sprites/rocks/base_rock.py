from setting import *
import pygame
import random
from ..power_up import Power_up

class BaseRock(pygame.sprite.Sprite):
    def __init__(self, game: 'Game'):
      
        super().__init__()
        self.res = game.res
        self.game = game
        self._layer = 1  # 圖層深度：隕石在最下面
        self.game.rocks.add(self)
        self.game.all_sprites.add(self)

        self.image_ori = random.choice(self.res['img']['rocks'])
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 // 2
        self.damage = self.radius
        self.health = 1
        # 初始位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(ROCK_SPAWN_Y_MIN, ROCK_SPAWN_Y_MAX)
        self.speedy = random.randrange(ROCK_MIN_SPEED_Y, ROCK_MAX_SPEED_Y)
        self.speedx = random.randrange(*ROCK_SPEED_X_RANGE)
        self.total_degree = 0
        self.rot_degree = random.randrange(*ROCK_ROT_DEGREE_RANGE)

    def destroy(self, game, Explosion):
        # 加分
        game.score += int(self.radius)
        
        # 播放爆炸音效
        expl_sound = random.choice(self.res['sound']['expls'])
        expl_sound.set_volume(0.5)
        expl_sound.play()

        # 產生爆炸動畫
        expl = Explosion(game, self.rect.center, 'lg')
        game.all_sprites.add(expl)

        # 隨機產生寶物
        if random.random() > 0.9:
            power = Power_up(game, self.rect.center)
            game.all_sprites.add(power)
            game.powers.add(power)

        # 摧毀自己
        self.kill()

    # 隕石旋轉
    def rotate(self):
        # 效能優化：如果隕石還在螢幕外面（還沒掉下來或已經飛走），就不要轉它
        # 因為 transform.rotate 是很吃力的數學運算，對看不見的東西做運算純屬浪費
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right > WIDTH or self.rect.right < 0:
            return

        # 處理隕石的旋轉動畫
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        # 更新隕石的位置和狀態
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # 邊界控制：如果超出螢幕，重置位置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(ROCK_SPAWN_Y_MAX, -40) 
            self.speedy = random.randrange(ROCK_MIN_SPEED_Y, ROCK_MAX_SPEED_Y)
            self.speedx = random.randrange(*ROCK_SPEED_X_RANGE)
