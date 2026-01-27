from setting import HEIGHT
import pygame
import pygame
import random
import os
from setting import *
from sprites import Player,Rock,Bullet
#遊戲初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('雷霆戰機')

#加載圖片
background_img = pygame.image.load(os.path.join('image','background.png')).convert()
background_img = pygame.transform.scale(background_img,(WIDTH,HEIGHT))
player_img = pygame.image.load(os.path.join('image','player.png')).convert()
bullet_img = pygame.image.load(os.path.join('image','bullet.png')).convert()
rocks_img = []
for i in range(7):
    rocks_img.append(pygame.image.load(os.path.join('image',f'rock{i}.png')).convert())

#加載音樂
shoot_sound = pygame.mixer.Sound(os.path.join('sound','shoot.wav'))
expl_sounds = [
pygame.mixer.Sound(os.path.join('sound','expl0.wav')),
pygame.mixer.Sound(os.path.join('sound','expl1.wav'))
]
pygame.mixer_music.load(os.path.join('sound','background.ogg'))
#調整音量
shoot_sound.set_volume(0.5)
pygame.mixer_music.set_volume(0.3)
#載入字體
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

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

#分數
score = 0

#播放背景音樂
pygame.mixer_music.play(-1)
#遊戲迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #自動射擊
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_SPACE]:
        player.shoot(all_sprites, bullets, bullet_img,  shoot_sound)
    # 更新全部的物件
    all_sprites.update()
    #石頭和子彈的碰撞
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)

    for hit in hits:
        expl_sound = random.choice(expl_sounds)
        expl_sound.set_volume(0.5)
        expl_sound.play()
        score += int(hit.radius)
        r = Rock(rocks_img)
        all_sprites.add(r)
        rocks.add(r)

    #飛機和石頭的碰撞
    hits = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hits:
        running = False

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(background_img, (0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH // 2 , 0)
    pygame.display.update()

pygame.quit()