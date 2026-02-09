import os
import pygame
from resource_manager import BASE_DIR
from setting import *

#載入字體
font_name = os.path.join(BASE_DIR, 'font', 'font.ttf')
def Draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

#顯示生命值
def Draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def Draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

#初始畫面
def Draw_init(surf, res):
    clock = pygame.time.Clock()

    surf.blit(res['img']['background'], (0, 0))
    Draw_text(surf, '太空生存戰!!!',64 ,WIDTH / 2, HEIGHT / 4)
    Draw_text(surf, 'AD鍵控制左右移動，空白鍵可以射擊。',23 , WIDTH / 2, HEIGHT / 2)
    Draw_text(surf, '點任意鍵可以開始遊戲。',23 , WIDTH / 2, (HEIGHT / 3) * 2)
    pygame.display.update()
    #初始化的迴圈
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

def Draw_end_screen(surf, res, score):
    surf.blit(res['img']['background'], (0,0))
    Draw_text(surf, '遊戲結束!', 64, WIDTH / 2, HEIGHT / 4)
    Draw_text(surf, f'最終分數: {score}.', 30, WIDTH / 2, HEIGHT / 2)
    Draw_text(surf, '按下 [R] 重新開始', 23, WIDTH / 2, (HEIGHT / 3) * 2)
    Draw_text(surf, '按下 [M] 回到主選單', 23, WIDTH / 2, (HEIGHT / 3) * 2 + 40)
    pygame.display.update()
    #結算畫面的迴圈
    waiting = True
    while waiting:
        pygame.time.Clock().tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'QUIT'
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    return 'RESTART'
                if event.key == pygame.K_m:
                    return 'MENU'