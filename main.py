import pygame
import random
from setting import *
from sprites import Player, Explosion, Power_up, BaseRock, SplitRock, ExplodingRock
from resource_manager import Load_resources
from ui_utils import Draw_text, Draw_health, Draw_lives, Draw_init, Draw_end_screen

#遊戲初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('飛機打隕石')

#圖片和音效的字典
res = Load_resources()

class Game:
    def __init__(self, res):
        self.res = res
        self.reset()

    def reset(self):
        # 創立各物件的群組，方便做碰撞判斷
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()

        # 生成各物件
        self.player = Player(self.res)
        self.all_sprites.add(self.player)

        for _ in range(10):
            self.new_rock()
        self.score = 0

    #增加石頭
    def new_rock(self):
        if len(self.rocks) >= MAX_ROCKS: 
            return

        spawn_rates = {
            'base': 50,
            'split': 30,
            'exploding':20
        }

        rock_type = random.choices(list(spawn_rates.keys()), weights = list(spawn_rates.values()), k = 1)[0]
        if rock_type == 'base':
            r = BaseRock(self.res)
        elif rock_type == 'split':
            r = SplitRock(self.res)
        elif rock_type == 'exploding':
            r = ExplodingRock(self.res)
        
        self.all_sprites.add(r)
        self.rocks.add(r)

game = Game(res)
#播放背景音樂
pygame.mixer_music.play(-1)
#遊戲迴圈
death_expl = None
show_init = True
running = True
while running:
    #初始畫面
    if show_init:
        Draw_init(screen, res)
        show_init = False

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #自動射擊
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_SPACE]:
        game.player.shoot(game.all_sprites, game.bullets)
    # 自動補充隕石 (維持 MIN_ROCKS~MAX_ROCKS 顆)
    while len(game.rocks) < MIN_ROCKS:
        game.new_rock()

    # 更新全部的物件
    game.all_sprites.update()

    #石頭和子彈的碰撞
    hits = pygame.sprite.groupcollide(game.rocks,game.bullets,True,True)
    for hit in hits:
        hit.destroy(game, Explosion, Power_up)
        

    #飛機和石頭的碰撞
    if not game.player.is_invincibility:
        hits = pygame.sprite.spritecollide(game.player,game.rocks,True,pygame.sprite.collide_circle)
        for hit in hits:
            game.player.health -= hit.radius
            expl = Explosion(hit.rect.center, 'sm', res)
            game.all_sprites.add(expl)
            res['sound']['crash_player'].play()
            if game.player.health <= 0:
                death_expl = Explosion(game.player.rect.center, 'player_die', res)
                game.all_sprites.add(death_expl)
                res['sound']['player_die'].play()
                game.player.lives -= 1
                if game.player.lives != 0:
                    game.player.health = 100
                    game.player.respawn()

    #結算畫面
    if game.player.lives <= 0:
        if death_expl is not None and not death_expl.alive():
            #玩家結算畫面的選擇
            action = Draw_end_screen(screen, res, game.score)

            if action == 'RESTART': #重新遊戲
                show_init = False
                game.reset()
            elif action == 'MENU':
                show_init = True # 回到初始遊戲介面
                game.reset()
            elif action == 'QUIT':
                running = False #退出遊戲

    # 飛機和寶物的碰撞
    hits = pygame.sprite.spritecollide(game.player, game.powers, True)
    for hit in hits:
        if hit.type == 'heal':
            game.player.health += 20
            if game.player.health > 100:
                game.player.health = 100
            res['sound']['power_up_sound']['heal'].play()
        elif hit.type == 'grade_up':
            game.player.grade_up()
            res['sound']['power_up_sound']['grade_up'].play()

    #畫面顯示
    screen.blit(res['img']['background'], (0,0))
    Draw_health(screen, game.player.health, 5, 15)
    game.all_sprites.draw(screen)
    Draw_lives(screen, game.player.lives, res['img']['player_mini'], WIDTH - 100, 15)
    Draw_text(screen, str(game.score), 18, WIDTH // 2 , 0)
    pygame.display.update()

pygame.quit()