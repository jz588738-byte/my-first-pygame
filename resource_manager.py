import pygame
import os
from setting import  *

#取得目前的檔案目錄
BASE_DIR = os.path.dirname(__file__)

def Load_resources():
    res = {
        'img': {},
        'power_up_img': {},
        'sound': {
            'power_up_sound':{}
        },
        'anim': {'lg': [], 'sm': [], 'player_die': []}
    }

    #加載圖片
    res['img']['background'] = pygame.image.load(os.path.join(BASE_DIR, 'image','background.png')).convert()
    res['img']['background'] = pygame.transform.scale(res['img']['background'],(WIDTH,HEIGHT))
    res['img']['player'] = pygame.image.load(os.path.join(BASE_DIR, 'image','player.png')).convert()
    res['img']['player_mini'] = pygame.image.load(os.path.join(BASE_DIR, 'image','player.png')).convert()
    res['img']['player_mini'] = pygame.transform.scale(res['img']['player_mini'], (20, 19))
    res['img']['bullet'] = pygame.image.load(os.path.join(BASE_DIR, 'image','bullet.png')).convert()
    #寶物圖片
    res['power_up_img']['grade_up'] = pygame.image.load(os.path.join(BASE_DIR, 'image','grade_up.png')).convert()
    res['power_up_img']['heal'] = pygame.image.load(os.path.join(BASE_DIR, 'image','heal.png')).convert()

    res['img']['rocks'] = []
    for i in range(7):
        res['img']['rocks'].append(pygame.image.load(os.path.join(BASE_DIR, 'image',f'rock{i}.png')).convert())

    #爆炸的動畫圖片
    for i in range(9):
        expl_img = pygame.image.load(os.path.join(BASE_DIR, 'image',f'expl{i}.png')).convert()
        expl_img.set_colorkey(BLACK)
        res['anim']['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
        res['anim']['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

        player_expl_img = pygame.image.load(os.path.join(BASE_DIR, 'image', f'player_expl{i}.png')).convert()
        player_expl_img.set_colorkey(BLACK)
        res['anim']['player_die'].append(player_expl_img)

    #加載音樂
    res['sound']['shoot'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','shoot.wav'))
    res['sound']['player_die'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','rumble.ogg'))
    res['sound']['power_up_sound']['grade_up'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','grade_up.wav'))
    res['sound']['power_up_sound']['heal'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound', 'heal.wav'))
    res['sound']['expls'] = [
    pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','expl0.wav')),
    pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','expl1.wav'))
    ]
    res['sound']['crash_player'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound', 'crash_player.wav'))

    pygame.mixer_music.load(os.path.join(BASE_DIR, 'sound','background.ogg'))

    return res