import pygame
import random
import os
from setting import *
from sprites import Player,Rock,Bullet
#遊戲初始化
pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('雷霆戰機')

#加載圖片
background = pygame.image.load(os.path.join('image','background.png')).convert()
player_img = pygame.image.load(os.path.join('image','player.png')).convert()
bullet_img = pygame.image.load(os.path.join('image','bullet.png')).convert()
rocks_img = []
for i in range(7):
    rocks_img.append(pygame.image.load(os.path.join('image',f'rock{i}.png')).convert())

#創立各物件的群組，方便做碰撞判斷
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#生成各物件
player = Player(player_img, bullet_img, all_sprites, bullets)
all_sprites.add(player)
for _ in range(10):
    r = Rock(rocks_img)
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
    #自動射擊
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_SPACE]:
        player.shoot(all_sprites, bullets, bullet_img)

    all_sprites.update()
    #石頭和子彈的碰撞
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        r = Rock(rocks_img)
        all_sprites.add(r)
        rocks.add(r)
    #飛機和石頭的碰撞
    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running = False
    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background, (0,0))
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()