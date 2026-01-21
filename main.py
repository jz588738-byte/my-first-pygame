import pygame
import random

#遊戲初始化
pygame.init()
#設定
FPS = 60
WIDTH = 600
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('雷霆戰機')
#顏色
WHITE = (255,255,255)
GREEN = (0,255,0)
RAD = (255,0,0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,40))
        self.image.fill(RAD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,4)
        self.speedx = random.randrange(-2, 2)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(2, 5)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(10):
    rock = Rock()
    all_sprites.add(rock)

#遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲
    all_sprites.update()
    #畫面顯示
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()