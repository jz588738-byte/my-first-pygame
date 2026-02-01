import pygame
import random
from setting import *
from sprites import Player, Rock, Explosion, Power_up
from resource_manager import Load_resources
from ui_utils import Draw_text, Draw_health, draw_lives

#遊戲初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('雷霆戰機')

#圖片和音效的字典
res = Load_resources()

#增加石頭
def new_rock():
    r = Rock(res)
    all_sprites.add(r)
    rocks.add(r)

#創立各物件的群組，方便做碰撞判斷
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powers = pygame.sprite.Group()

#生成各物件
player = Player(res)
all_sprites.add(player)
for _ in range(10):
    new_rock()

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
        player.shoot(all_sprites, bullets)
    # 更新全部的物件
    all_sprites.update()

    #石頭和子彈的碰撞
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hit in hits:
        expl_sound = random.choice(res['sound']['expls'])
        expl_sound.set_volume(0.5)
        expl_sound.play()
        score += int(hit.radius)
        expl = Explosion(hit.rect.center, 'lg', res)
        all_sprites.add(expl)
        if random.random() > 0.92:
            power = Power_up(res, hit.rect.center)
            all_sprites.add(power)
            powers.add(power)
        new_rock()

    #飛機和石頭的碰撞
    hits = pygame.sprite.spritecollide(player,rocks,True,pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm', res)
        all_sprites.add(expl)
        res['sound']['crash_player'].play()
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player_die', res)
            all_sprites.add(death_expl)
            res['sound']['player_die'].play()
            player.lives -= 1
            player.health = 100
            player.respawn()

    # 飛機和石頭的碰撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'heal':
            player.health += 20
            if player.health > 100:
                player.health = 100
            res['sound']['power_up_sound']['heal'].play()
        elif hit.type == 'grade_up':
            player.grade_up()
            res['sound']['power_up_sound']['grade_up'].play()
    if player.lives == 0 and not death_expl.alive():
        running = False

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(res['img']['background'], (0,0))
    Draw_health(screen, player.health, 5, 15)
    all_sprites.draw(screen)
    draw_lives(screen, player.lives, res['img']['player_mini'], WIDTH - 100, 15)
    Draw_text(screen, str(score), 18, WIDTH // 2 , 0)
    pygame.display.update()

pygame.quit()