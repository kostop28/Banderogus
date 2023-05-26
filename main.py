import pygame

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT #, K_TAB
import random
from os import listdir

#from pygame.cursors import ball

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (153, 135, 48)

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

img_index = 0

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[0]
ball_rect = player.get_rect()
ball_speed = 5

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint (0, height-50), *enemy.get_size())
    enemy_speed = random.randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint (0, width-150),-250, *bonus.get_size())
    bonus_speed = random.randint(1, 4)
    return [bonus, bonus_rect, bonus_speed]

def create_boss():
    boss = pygame.image.load('boss1.png').convert_alpha()
    boss_rect = pygame.Rect(width, random.randint (0, height-250), *boss.get_size())
    boss_speed = random.randint(5, 10)
    return [boss, boss_rect, boss_speed]

bg= pygame.transform.scale( pygame.image.load('background.png').convert(),screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 2

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 1500))

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, random.randint(1000, 2500))

CREATE_BOSS = pygame.USEREVENT + 4
pygame.time.set_timer(CREATE_BOSS, random.randint(12500, 20000))

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

enemies = []

bonuses = []

bosses = []

scores = 0

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

        if event.type == CREATE_BOSS:
            bosses.append(create_boss())

    pressed_keys = pygame.key.get_pressed()

    bgx -= bg_speed
    bgx2 -= bg_speed

    if bgx < -bg.get_width():
        bgx = bg.get_width()

    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))

    main_surface.blit(player,ball_rect)

    main_surface.blit(font.render('Score: ' + str(scores), True, GOLD ), (width -100 , 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0],enemy[1])

        if enemy[1].left < 0-200:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0],bonus[1])

        if bonus[1].top > height:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

        for enemy in enemies:
            if bonus[1].colliderect(enemy[1]):
                bonuses.pop(bonuses.index(bonus))
                break

    for boss in bosses:
        boss[1] = boss[1].move(-boss[2], 0)
        main_surface.blit(boss[0], boss[1])
        if boss[1].left < 0 - 200:
            bosses.pop(bosses.index(boss))
        if ball_rect.colliderect(boss[1]):
            is_working = False


    if pressed_keys [K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0,ball_speed)

    if pressed_keys [K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0,-ball_speed)

    if pressed_keys [K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed,0)

    if pressed_keys [K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed,0)

    #if pressed_keys [K_TAB]:
    #     ball_speed = 0
    #     boss_speed = 0
    #     enemy_speed = 0
    #     bonus_speed = 0
    #
    #     CREATE_ENEMY = pygame.USEREVENT + 1
    #     pygame.time.set_timer(CREATE_ENEMY, 0)
    #
    #     CREATE_BONUS = pygame.USEREVENT + 2
    #     pygame.time.set_timer(CREATE_BONUS, 0)
    #
    #     CREATE_BOSS = pygame.USEREVENT + 4
    #     pygame.time.set_timer(CREATE_BOSS, 0)
    #
    #     CHANGE_IMG = pygame.USEREVENT + 3
    #     pygame.time.set_timer(CHANGE_IMG, 0)
    #
    # if pressed_keys [K_TAB] and ball_speed == 0  :
    #     ball_speed = 5
    #     boss_speed = random.randint(5, 10)
    #     enemy_speed = random.randint(3, 5)
    #     bonus_speed = random.randint(1, 4)
    #
    #     CREATE_ENEMY = pygame.USEREVENT + 1
    #     pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 1500))
    #
    #     CREATE_BONUS = pygame.USEREVENT + 2
    #     pygame.time.set_timer(CREATE_BONUS, random.randint(1000, 2500))
    #
    #     CREATE_BOSS = pygame.USEREVENT + 4
    #     pygame.time.set_timer(CREATE_BOSS, random.randint(12500, 20000))
    #
    #     CHANGE_IMG = pygame.USEREVENT + 3
    #     pygame.time.set_timer(CHANGE_IMG, 200)


    pygame.display.flip()