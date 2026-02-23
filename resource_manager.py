import pygame
import os
from setting import  *

#取得目前的檔案目錄
BASE_DIR = os.path.dirname(__file__)

def Load_resources():
    res = {
        'img': {},
        'power_up_img': {},
        'font':{},
        'sound': {
            'power_up_sound':{}
        },
        'anim': {'lg': [], 'sm': [], 'player_die': [], 'damage_exploding': []}
    }

    #加載圖片
    res['img']['background'] = pygame.image.load(os.path.join(BASE_DIR, 'image','background.png')).convert()
    res['img']['background'] = pygame.transform.scale(res['img']['background'],(WIDTH,HEIGHT))
    res['img']['player'] = pygame.image.load(os.path.join(BASE_DIR, 'image','player.png')).convert()
    res['img']['player'].set_colorkey(BLACK)
    res['img']['player_mini'] = pygame.image.load(os.path.join(BASE_DIR, 'image','player.png')).convert()
    res['img']['player_mini'].set_colorkey(BLACK)
    res['img']['player_mini'] = pygame.transform.scale(res['img']['player_mini'], (20, 19))
    res['img']['bullet'] = pygame.image.load(os.path.join(BASE_DIR, 'image','bullet.png')).convert()
    res['img']['bullet'].set_colorkey(BLACK)
    #寶物圖片
    res['power_up_img']['grade_up'] = pygame.image.load(os.path.join(BASE_DIR, 'image','grade_up.png')).convert()
    res['power_up_img']['grade_up'].set_colorkey(BLACK)
    res['power_up_img']['heal'] = pygame.image.load(os.path.join(BASE_DIR, 'image','heal.png')).convert()
    res['power_up_img']['heal'].set_colorkey(BLACK)

    #隕石圖片
    res['img']['rocks'] = []
    for i in range(7):
        img = pygame.image.load(os.path.join(BASE_DIR, 'image',f'rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['rocks'].append(img)
    
    res['img']['split_rocks'] = []
    for i in range(3):
        img = pygame.image.load(os.path.join(BASE_DIR, 'image',f'split_rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['split_rocks'].append(img)

    res['img']['exploding_rock'] = []
    for i in range(3):
        img = pygame.image.load(os.path.join(BASE_DIR, 'image',f'exploding_rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['exploding_rock'].append(img)
    #爆炸的動畫圖片
    for i in range(9):
        expl_img = pygame.image.load(os.path.join(BASE_DIR, 'image',f'expl{i}.png')).convert_alpha()
        res['anim']['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
        res['anim']['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

        player_expl_img = pygame.image.load(os.path.join(BASE_DIR, 'image', f'player_expl{i}.png')).convert_alpha()
        res['anim']['player_die'].append(player_expl_img)
    
    for i in range(1, 10):
        damage_exploding_img = pygame.image.load(os.path.join(BASE_DIR, 'image', f'damage_exploding ({i}).png')).convert_alpha()
        res['anim']['damage_exploding'].append(damage_exploding_img)

    #加載音樂
    res['sound']['shoot'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','shoot.wav'))
    res['sound']['player_die'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','rumble.ogg'))
    res['sound']['power_up_sound']['grade_up'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','grade_up.wav'))
    res['sound']['power_up_sound']['heal'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound', 'heal.wav'))
    res['sound']['damage_exploding'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound', 'damage_exploding.wav'))
    res['sound']['expls'] = [
    pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','expl0.wav')),
    pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound','expl1.wav'))
    ]
    res['sound']['crash_player'] = pygame.mixer.Sound(os.path.join(BASE_DIR, 'sound', 'crash_player.wav'))

    pygame.mixer_music.load(os.path.join(BASE_DIR, 'sound','background.ogg'))

    return res