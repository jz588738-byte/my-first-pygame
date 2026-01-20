import pygame

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2,HEIGHT // 2)
        self.rect.x = 400
        self.rect.y = 400

    def update(self):
        self.rect.x += 2
        if self.rect.left > WIDTH:
            self.rect.right = 0

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)


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