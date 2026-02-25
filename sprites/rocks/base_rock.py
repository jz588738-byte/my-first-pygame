from setting import *
import pygame
import random

class BaseRock(pygame.sprite.Sprite):
    """
    遊戲中的基本隕石物件。

    繼承自 pygame.sprite.Sprite，負責處理隕石的移動、旋轉和繪製。
    """
    def __init__(self, res: dict):
        """
        初始化隕石。

        Args:
            res (dict): 包含遊戲資源（圖片、音效）的字典。
        """
        super().__init__()
        self.res = res
        self.image_ori = random.choice(self.res['img']['rocks'])
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85 // 2
        # 初始位置
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(ROCK_SPAWN_Y_MIN, ROCK_SPAWN_Y_MAX)
        self.speedy = random.randrange(ROCK_MIN_SPEED_Y, ROCK_MAX_SPEED_Y)
        self.speedx = random.randrange(*ROCK_SPEED_X_RANGE)
        self.total_degree = 0
        self.rot_degree = random.randrange(*ROCK_ROT_DEGREE_RANGE)

    def destroy(self, game, Explosion, Power_up):
        """處理隕石被摧毀的邏輯。"""
        # 加分
        game.score += int(self.radius)
        
        # 播放爆炸音效
        expl_sound = random.choice(self.res['sound']['expls'])
        expl_sound.set_volume(0.5)
        expl_sound.play()

        # 產生爆炸動畫
        expl = Explosion(self.rect.center, 'lg', self.res)
        game.all_sprites.add(expl)

        # 隨機產生寶物
        if random.random() > 0.9:
            power = Power_up(self.res, self.rect.center)
            game.all_sprites.add(power)
            game.powers.add(power)

        # 摧毀自己
        self.kill()

    # 隕石旋轉
    def rotate(self):
        """處理隕石的旋轉動畫。"""
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        """更新隕石的位置和狀態。"""
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # 邊界控制：如果超出螢幕，重置位置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(ROCK_SPAWN_Y_MAX, -40) # 重生位置稍微調整
            self.speedy = random.randrange(ROCK_MIN_SPEED_Y, ROCK_MAX_SPEED_Y)
            self.speedx = random.randrange(*ROCK_SPEED_X_RANGE)
