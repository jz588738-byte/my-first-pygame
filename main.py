import pygame
import random
from setting import *
from sprites import *
from resource_manager import Load_resources
from ui_utils import Draw_text, Draw_health, Draw_lives, Draw_init, Draw_end_screen

#遊戲初始化
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
#名字
pygame.display.set_caption('飛機打隕石')

# 載入資源
res = Load_resources()

class Game:
    def __init__(self, res, screen):
        self.res = res
        self.screen = screen
        self.reset()

    def reset(self):
        # 創立各物件的群組 (使用 LayeredUpdates 來管理誰在誰上面)
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        # 生成玩家
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for _ in range(10):
            self.new_enemy()
        
        self.score = 0

    #增加石頭
    def new_enemy(self):
        if len(self.rocks) >= MAX_ROCKS: 
            return

        spawn_rates = {
            BaseRock: 40,
            SplitRock: 30,
            ExplodingRock:20,
            Sniper:10
        }

        enemy_class = random.choices(list(spawn_rates.keys()), weights=list(spawn_rates.values()), k=1)[0]
        enemy_class(self)

    def draw(self, screen):
        # 1. 畫背景
        screen.blit(self.res['img']['background'], (0,0))
        
        # 繪製所有精靈
        self.all_sprites.draw(self.screen)
        
        for enemy in self.enemies:
            if hasattr(enemy, 'draw_extras'):
                enemy.draw_extras(self.screen)
        
        # 4. 畫 UI
        Draw_health(screen, self.player.health, 5, 15)
        Draw_lives(screen, self.player.lives, self.res['img']['player_mini'], WIDTH - 100, 15)
        Draw_text(screen, str(self.score), 18, WIDTH // 2 , 0)

# 建立遊戲實例
game = Game(res, screen)
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
    
    while len(game.rocks) + len(game.enemies) < MIN_ROCKS:
        game.new_enemy()

    # 更新全部物件狀態
    game.all_sprites.update()

    #石頭和玩家子彈的碰撞
    hits = pygame.sprite.groupcollide(game.rocks, game.bullets, False, True)
    for hit in hits:
        hit.health -= 1
        if hit.health <= 0:
            hit.destroy(game, Explosion)

    # 子彈與敵機
    hits = pygame.sprite.groupcollide(game.enemies, game.bullets, False, True)
    for hit in hits:
        if hasattr(hit, 'take_damage'):
            hit.take_damage(1)

    # 玩家與危險物 (石頭/敵人/雷射)
    if not game.player.is_invincibility:
        # 石頭碰撞 (撞到就移除)
        hits_rocks = pygame.sprite.spritecollide(game.player, game.rocks, True, pygame.sprite.collide_circle)
        # 敵機碰撞
        hits_enemies = pygame.sprite.spritecollide(game.player, game.enemies, False, pygame.sprite.collide_circle)
        # 雷射碰撞 
        hits_lasers = pygame.sprite.spritecollide(game.player, game.lasers, False, pygame.sprite.collide_mask)
        
        all_hits = hits_rocks + hits_enemies + hits_lasers
        for hit in all_hits:
            # 判斷是否為雷射，如果是且已經造成過傷害或是非第一幀，就跳過
            if hit in hits_lasers:
                if hit.has_damaged_player or hit.frame != 0:
                    continue
                else:
                    hit.has_damaged_player = True

            game.player.health -= hit.damage
            
            # 如果是被雷射打到，爆炸位置應該在玩家身上，而不是在雷射的中心點
            expl_pos = game.player.rect.center if hit in hits_lasers else hit.rect.center
            expl = Explosion(game, expl_pos, 'sm')
            
            game.all_sprites.add(expl)
            res['sound']['crash_player'].play()
            
            # 如果撞到的是敵機，敵機也受損
            if hit in hits_enemies and hasattr(hit, 'take_damage'):
                hit.take_damage(100)

            if game.player.health <= 0:
                death_expl = Explosion(game, game.player.rect.center, 'player_die')
                game.all_sprites.add(death_expl)
                res['sound']['player_die'].play()
                game.player.lives -= 1
                if game.player.lives > 0:
                    game.player.health = 100
                    game.player.respawn()

    # 玩家與寶物
    hits = pygame.sprite.spritecollide(game.player, game.powers, True)
    for hit in hits:
        if hit.type == 'heal':
            game.player.health = min(100, game.player.health + 20)
            res['sound']['power_up_sound']['heal'].play()
        elif hit.type == 'grade_up':
            game.player.grade_up()
            res['sound']['power_up_sound']['grade_up'].play()

    # 6. 死亡與遊戲結束判定
    if game.player.lives <= 0:
        if death_expl is not None and not death_expl.alive():
            action = Draw_end_screen(screen, res, game.score)
            if action == 'RESTART':
                show_init = False
                game.reset()
            elif action == 'MENU':
                show_init = True
                game.reset()
            elif action == 'QUIT':
                running = False

    # 7. 畫面重繪
    game.draw(screen)
    pygame.display.update()

pygame.quit()