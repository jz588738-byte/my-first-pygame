import pygame
from state_machine import State
from ui_utils import Draw_text, Draw_health, Draw_lives
from setting import *
from sprites import *

class GameBaseState(State):
    def __init__(self, owner, game):
        super().__init__(owner)
        self.game = game 
        self.res = game.res
        self.screen = game.screen

class MenuState(GameBaseState):
    def enter(self):
        pygame.mixer.music.play(-1)

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYUP:
                self.owner.state_machine.change_state("PlayState")
        
    def draw(self, screen):
        screen.blit(self.res['img']['background'], (0, 0))
        Draw_text(screen, '太空生存戰!!!', 64, WIDTH / 2, HEIGHT / 4)
        Draw_text(screen, 'AD鍵控制左右移動，空白鍵可以射擊。', 23, WIDTH / 2, HEIGHT / 2)
        Draw_text(screen, '點任意鍵可以開始遊戲。', 23, WIDTH / 2, (HEIGHT / 3) * 2)

class PlayState(GameBaseState):
    def enter(self):
        self.game.reset()
        pygame.mixer.music.play(-1)

    def update(self, dt, events=None):
        game = self.game

        # 自動射擊
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            game.player.shoot(game.all_sprites, game.bullets)
        
        # 補充敵人
        while len(game.rocks) + len(game.enemies) < MIN_ROCKS:
            game.new_enemy()

        # 更新所有精靈
        game.all_sprites.update(dt)

        # ── 碰撞處理 ──
        # 石頭 vs 子彈
        hits = pygame.sprite.groupcollide(game.rocks, game.bullets, False, True)
        for hit in hits:
            hit.health -= 1
            if hit.health <= 0:
                hit.destroy(game, Explosion)

        # 敵機 vs 子彈
        hits = pygame.sprite.groupcollide(game.enemies, game.bullets, False, True)
        for hit in hits:
            if hasattr(hit, 'take_damage'):
                hit.take_damage(1)

        # 玩家 vs 危險物
        if not game.player.is_invincibility:
            hits_rocks = pygame.sprite.spritecollide(game.player, game.rocks, True, pygame.sprite.collide_circle)
            hits_enemies = pygame.sprite.spritecollide(game.player, game.enemies, False, pygame.sprite.collide_circle)
            hits_lasers = pygame.sprite.spritecollide(game.player, game.lasers, False, pygame.sprite.collide_mask)
            
            all_hits = hits_rocks + hits_enemies + hits_lasers
            for hit in all_hits:
                if hit in hits_lasers:
                    if hit.has_damaged_player or hit.frame != 0:
                        continue
                    else:
                        hit.has_damaged_player = True
                
                expl_pos = game.player.rect.center if hit in hits_lasers else hit.rect.center
                _death_expl = game.player.take_damage(hit.damage, expl_pos)
                if _death_expl:
                    game.death_expl = _death_expl
                
                if hit in hits_enemies and hasattr(hit, 'take_damage'):
                    hit.take_damage(100)

        # 玩家 vs 寶物
        hits = pygame.sprite.spritecollide(game.player, game.powers, True)
        for hit in hits:
            if hit.type == 'heal':
                game.player.health = min(100, game.player.health + 20)
                self.res['sound']['power_up_sound']['heal'].play()
            elif hit.type == 'grade_up':
                game.player.grade_up()
                self.res['sound']['power_up_sound']['grade_up'].play()

        # 死亡判定
        if game.player.lives <= 0:
            if game.death_expl is not None and not game.death_expl.alive():
                self.owner.state_machine.change_state("GameOverState")

    def draw(self, screen):
        self.game.draw(screen)

class GameOverState(GameBaseState):
    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    self.owner.state_machine.change_state("PlayState")
                if event.key == pygame.K_m:
                    self.owner.state_machine.change_state("MenuState")
        
    def draw(self, screen):
        screen.blit(self.res['img']['background'], (0,0))
        Draw_text(screen, '遊戲結束!', 64, WIDTH / 2, HEIGHT / 4)
        Draw_text(screen, f'最終分數: {self.game.score}.', 30, WIDTH / 2, HEIGHT / 2)
        Draw_text(screen, '按下 [R] 重新開始', 23, WIDTH / 2, (HEIGHT / 3) * 2)
        Draw_text(screen, '按下 [M] 回到主選單', 23, WIDTH / 2, (HEIGHT / 3) * 2 + 40)