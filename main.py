import pygame
import random
import os
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
YELLOW = (255,255,0)
BLACK = (0,0,0)
#加載圖片
background = pygame.image.load(os.path.join('image','background.png')).convert()
player = pygame.image.load(os.path.join('image','player.png')).convert()
rock = pygame.image.load(os.path.join('image','rock.png')).convert()
bullet = pygame.image.load(os.path.join('image','bullet.png')).convert()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        #自動射擊
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        #鍵盤控制邏輯
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        #自動射擊
        if key_pressed[pygame.K_SPACE]:
            self.shoot()
        #邊界控制
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = rock
        self.image.set_colorkey(BLACK)
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = bullet
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for _ in range(10):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

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
    #石頭和子彈的碰撞
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)
    #飛機和石頭的碰撞
    hits = pygame.sprite.spritecollide(player,rocks,False)
    if hits:
        running = False
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()