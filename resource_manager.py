from setting import BLACK, WIDTH, HEIGHT  # 確保導入 WIDTH, HEIGHT
import pygame
import os

# 在網頁版中，路徑最好直接從 assets 開始
def Load_resources():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    IMAGE_DIR = os.path.join(BASE_DIR, 'assets', 'image')
    SOUND_DIR = os.path.join(BASE_DIR, 'assets', 'sound')

    res = {
        'img': {},
        'power_up_img': {},
        'font':{},
        'sound': {
            'power_up_sound':{}
        },
        'anim': {'lg': [], 'sm': [], 'player_die': [], 'damage_exploding': []}
    }

    # --- 圖片載入 ---
    # 加上 assets/ 字樣，並確保路徑與你的資料夾名稱完全一致
    res['img']['background'] = pygame.image.load(os.path.join(IMAGE_DIR, 'background.png')).convert()
    res['img']['background'] = pygame.transform.scale(res['img']['background'], (WIDTH, HEIGHT))
    
    res['img']['player'] = pygame.image.load(os.path.join(IMAGE_DIR, 'player.png')).convert()
    res['img']['player'].set_colorkey(BLACK)
    
    res['img']['player_mini'] = pygame.transform.scale(res['img']['player'], (20, 19))
    
    res['img']['bullet'] = pygame.image.load(os.path.join(IMAGE_DIR, 'bullet.png')).convert()
    res['img']['bullet'].set_colorkey(BLACK)

    # 寶物
    res['power_up_img']['grade_up'] = pygame.image.load(os.path.join(IMAGE_DIR, 'grade_up.png')).convert()
    res['power_up_img']['grade_up'].set_colorkey(BLACK)
    res['power_up_img']['heal'] = pygame.image.load(os.path.join(IMAGE_DIR, 'heal.png')).convert()
    res['power_up_img']['heal'].set_colorkey(BLACK)

    # 敵機
    res['img']['sniper'] = pygame.image.load(os.path.join(IMAGE_DIR, 'sniper.png')).convert()
    res['img']['sniper'] = pygame.transform.scale(res['img']['sniper'], (50, 50))
    res['img']['sniper'].set_colorkey(BLACK)
    
    res['img']['rusher'] = pygame.image.load(os.path.join(IMAGE_DIR, 'rusher.png')).convert()
    res['img']['rusher'] = pygame.transform.scale(res['img']['rusher'], (50, 50))
    res['img']['rusher'].set_colorkey(BLACK)
    
    res['img']['rusher_go'] = pygame.image.load(os.path.join(IMAGE_DIR, 'rusher_go.png')).convert()
    res['img']['rusher_go'] = pygame.transform.scale(res['img']['rusher_go'], (50, 50))
    res['img']['rusher_go'].set_colorkey(BLACK)
    
    res['img']['rusher_burst'] = pygame.image.load(os.path.join(IMAGE_DIR, 'rusher_burst.png')).convert()
    res['img']['rusher_burst'] = pygame.transform.scale(res['img']['rusher_burst'], (50, 50))
    res['img']['rusher_burst'].set_colorkey(BLACK)

    # 隕石動畫 (迴圈也要改)
    res['img']['rocks'] = []
    for i in range(7):
        img = pygame.image.load(os.path.join(IMAGE_DIR, f'rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['rocks'].append(img)
    
    res['img']['split_rocks'] = []
    for i in range(3):
        img = pygame.image.load(os.path.join(IMAGE_DIR, f'split_rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['split_rocks'].append(img)

    res['img']['exploding_rock'] = []
    for i in range(3):
        img = pygame.image.load(os.path.join(IMAGE_DIR, f'exploding_rock{i}.png')).convert()
        img.set_colorkey(BLACK)
        res['img']['exploding_rock'].append(img)
    
    # 爆炸動畫
    for i in range(9):
        expl_img = pygame.image.load(os.path.join(IMAGE_DIR, f'expl{i}.png')).convert_alpha()
        res['anim']['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
        res['anim']['sm'].append(pygame.transform.scale(expl_img, (30, 30)))

        player_expl_img = pygame.image.load(os.path.join(IMAGE_DIR, f'player_expl{i}.png')).convert_alpha()
        res['anim']['player_die'].append(player_expl_img)
    
    for i in range(1, 10):
        damage_exploding_img = pygame.image.load(os.path.join(IMAGE_DIR, f'damage_exploding{i}.png')).convert_alpha()
        res['anim']['damage_exploding'].append(damage_exploding_img)

    res['anim']['laser'] = []
    for i in range(1, 7):
        laser_img = pygame.image.load(os.path.join(IMAGE_DIR, f'laser{i}.png')).convert()
        laser_img.set_colorkey(BLACK)
        res['anim']['laser'].append(laser_img)
    
    # --- 音樂載入 ---
    # 同樣補上 assets/sound/
    res['sound']['shoot'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'shoot.ogg'))
    res['sound']['player_die'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'rumble.ogg'))
    res['sound']['power_up_sound']['grade_up'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'grade_up.ogg'))
    res['sound']['power_up_sound']['heal'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'heal.ogg'))
    res['sound']['damage_exploding'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'damage_exploding.ogg'))
    res['sound']['expls'] = [
        pygame.mixer.Sound(os.path.join(SOUND_DIR, 'expl0.ogg')),
        pygame.mixer.Sound(os.path.join(SOUND_DIR, 'expl1.ogg'))
    ]
    res['sound']['rusher_boost'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'rusher_boost.ogg'))
    res['sound']['rusher_passby'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'rusher_passby.ogg'))
    res['sound']['crash_player'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'crash_player.ogg'))
    res['sound']['hit_enemy'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'hit_enemy.ogg'))
    res['sound']['laser_shoot'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'laser_shoot.ogg'))
    res['sound']['enemy_death'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'enemy_death.ogg'))
    res['sound']['charging'] = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'charging.ogg'))
    
    pygame.mixer_music.load(os.path.join(SOUND_DIR, 'background.ogg'))

    return res