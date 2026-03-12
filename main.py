import pygame
import random
from setting import *
from sprites import *
from resource_manager import Load_resources
from ui_utils import Draw_text, Draw_health, Draw_lives
from state_machine import StateMachine
from game_states import MenuState, PlayState, GameOverState

# ── 初始化 ──
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('飛機打隕石')

# ── 載入資源 ──
res = Load_resources()

class Game:
    def __init__(self, res, screen):
        self.res = res
        self.screen = screen
        self.death_expl = None

        # ── 建立 State Machine ──
        self.state_machine = StateMachine(self)
        self.state_machine.add_state("MenuState", MenuState(self, self))
        self.state_machine.add_state("PlayState", PlayState(self, self))
        self.state_machine.add_state("GameOverState", GameOverState(self, self))
        self.state_machine.change_state("MenuState")

    def reset(self):
        self.death_expl = None
        # 清空舊精靈
        if hasattr(self, 'all_sprites'):
            for s in list(self.all_sprites):
                s.kill()

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)
        for _ in range(10):
            self.new_enemy()

        self.score = 0

    def new_enemy(self):
        if len(self.rocks) >= MAX_ROCKS:
            return
        spawn_rates = {
            BaseRock: 40,
            SplitRock: 30,
            ExplodingRock: 20,
            Sniper: 10,
        }
        enemy_class = random.choices(list(spawn_rates.keys()), weights=list(spawn_rates.values()), k=1)[0]
        enemy_class(self)

    def draw(self, screen):
        screen.blit(self.res['img']['background'], (0, 0))
        self.all_sprites.draw(self.screen)
        for enemy in self.enemies:
            if hasattr(enemy, 'draw_extras'):
                enemy.draw_extras(self.screen)

        Draw_health(screen, self.player.health, 5, 15)
        Draw_lives(screen, self.player.lives, self.res['img']['player_mini'], WIDTH - 100, 15)
        Draw_text(screen, str(self.score), 18, WIDTH // 2, 0)

# 建立遊戲實例
game = Game(res, screen)

# ── 主迴圈 ──
running = True
while running:
    clock.tick(FPS)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # 全部交給狀態機處理
    game.state_machine.update(events)
    game.state_machine.draw(screen)
    pygame.display.update()

pygame.quit()