import pygame
import random
import math
from pygame import mixer

pygame.init()

# CONSTANTs
WIDTH, HEIGHT = 1000, 600
FPS = 60
# colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AZUL_MARINO = (27, 26, 54)
# player
PLAYER_B_X = WIDTH // 2 - 32
PLAYER_B_Y = HEIGHT - 104
PLAYER_WIDTH, PLAYER_HEIGHT = 64, 64
# speeds
SPEED = 5
ENEMY_SPEED = 6
BULLET_SPEED = 10
# enemy
ENEMY_WIDTH = 64
ENEMY_HEIGHT = 64
# enemy movement variables
plus = 55
first = 20
second = first + plus
third = second + plus
fourth = third + plus
fifth = fourth + plus
sixth = fifth + plus
seventh = sixth + plus
eight = seventh + plus
ninth = eight + plus
tenth = ninth + plus
eleventh = tenth + plus

bullets_fired = []
enemys_alive = []

# music and sound making
pygame.mixer.music.load('background1.wav')
mixer.music.set_volume(0.10)
mixer.music.play(-1)
music_playing = 'normal'
bullet_sound = mixer.Sound('laser.wav')
bullet_sound.set_volume(0.07)
explosion_sound = mixer.Sound('explosion.wav')
explosion_sound.set_volume(0.04)
# ereh XD
ereh_sound = mixer.Sound('EREH.wav')
ereh_sound.set_volume(0.10)
# king crimson
king_krimson = mixer.Sound('king_crimson.wav')
time = 0
# score display values
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

score_textX = 10
score_textY = 10

# GAME OVER
OVER_size = 100
fond = pygame.font.Font('freesansbold.ttf', OVER_size)
overX = WIDTH // 2 - OVER_size // 2 * 5
overY = HEIGHT // 2 - OVER_size // 2
game_over_text_done = None
GAMEOVER = False

# restart
restart_text = 32
restart_fond = pygame.font.Font('freesansbold.ttf', restart_text)
restart_X = 0
restart_Y = HEIGHT - restart_text

# life
life_time = 5
fond_life = pygame.font.Font('freesansbold.ttf', 32)
life_X = 0
life_Y = HEIGHT - 32

# create window and window tuples
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# icon and caption change
pygame.display.set_caption('space invaders')
RAW_ICON = pygame.image.load('001-spaceship.png')
pygame.display.set_icon(RAW_ICON)

# make the hit boxes
player_rect = pygame.Rect(PLAYER_B_X, PLAYER_B_Y, PLAYER_WIDTH, PLAYER_HEIGHT)

# take images from out
player_image = pygame.image.load('001-space-invaders.png')
enemy_image = pygame.image.load('enemy_alien.png')
player_bullet = pygame.image.load('002-bullet.png')
background = pygame.image.load('space_background.jpg')
pygame.transform.scale(background, (1000, 900))
mikasa = pygame.image.load('mikasa_chikita.png')
mikasa_width, mikasa_height = 64, 64
pygame.transform.scale(mikasa, (mikasa_width, mikasa_height))


def music_changing(wich, event):
    if wich == 'normal' and event.key == pygame.K_UP:
        mixer.music.load('fresh.wav')
        mixer.music.play(1)
        global music_playing
        music_playing = 'fresh'
    if wich == 'fresh' and event.key == pygame.K_n:
        mixer.music.load('background1.wav')
        mixer.music.play(-1)
        music_playing = 'normal'


def mikasa_ereh(ereh, event):
    if event.key == pygame.K_h:
        ereh.play()


def king_crimson(king, enemies, event):
    global time
    if time < 0:
        if event.key == pygame.K_RIGHT:
            time = 6
            king.play()
            for enemy in enemies:
                enemy.y += plus * 2
    time -= 0.08


def restart_texting(text, x, y):
    global GAMEOVER
    if GAMEOVER:
        texting = text.render('press R to restart', True, WHITE)
        WINDOW.blit(texting, (x, y))


def co_en_w_bullet(bullet_rect, enemy_rect):
    listi = []
    hit_zone = 25
    distancexone = math.sqrt(
        math.pow((enemy_rect.x + 20) - bullet_rect.x, 2) + math.pow((enemy_rect.y + 20) - bullet_rect.y, 2))
    distanceyone = math.sqrt(
        math.pow((enemy_rect.x + 20) - bullet_rect.x, 2) + math.pow((enemy_rect.y + 44) - bullet_rect.y, 2))
    distancextwo = math.sqrt(
        math.pow((enemy_rect.x + 44) - bullet_rect.x, 2) + math.pow(enemy_rect.y + 20 - bullet_rect.y, 2))
    distanceytwo = math.sqrt(
        math.pow((enemy_rect.x + 44) - bullet_rect.x, 2) + math.pow((enemy_rect.y + 44) - bullet_rect.y, 2))
    if distancexone <= hit_zone:
        listi.append(True)
    else:
        listi.append(False)
    if distanceyone <= hit_zone:
        listi.append(True)
    else:
        listi.append(False)
    if distancextwo <= hit_zone:
        listi.append(True)
    else:
        listi.append(False)
    if distanceytwo <= hit_zone:
        listi.append(True)
    else:
        listi.append(False)
    return listi


def bullets_and_enemys_handle(bullets, enemies_alive):
    for bullet in bullets:
        if bullet.y < 10:
            bullets.remove(bullet)
            continue
        for enemy in enemies_alive:
            collition = co_en_w_bullet(bullet, enemy)
            if collition[0] or collition[1] or collition[2] or collition[3]:
                explosion_sound.play()
                if bullet in bullets:
                    bullets.remove(bullet)
                enemies_alive.remove(enemy)
                global score_value
                score_value += 3
        if bullet.y - BULLET_SPEED > 0:
            bullet.y -= BULLET_SPEED


def player_movement(player, keys_pressed):
    if not GAMEOVER:
        global life_time
        if keys_pressed[pygame.K_a] and player.x - SPEED > 0:
            player.x -= SPEED
            life_time = 5
        if keys_pressed[pygame.K_d] and (player.x + PLAYER_WIDTH) + SPEED < WIDTH:
            player.x += SPEED
            life_time = 5


def create_enemys(enemys_alive):
    ENEMY_B_X = random.randint(20, WIDTH - 84)
    ENEMY_B_Y = random.randint(20, 130)
    if ENEMY_B_Y < 40:
        ENEMY_B_Y = 20
    elif ENEMY_B_Y >= 40 and ENEMY_B_Y < 101:
        ENEMY_B_Y = 75
    elif ENEMY_B_Y >= 101 and ENEMY_B_Y < 130:
        ENEMY_B_Y = 130
    if len(enemys_alive) < 10:
        enemy = pygame.Rect(ENEMY_B_X, ENEMY_B_Y, ENEMY_WIDTH, PLAYER_HEIGHT)
        enemys_alive.append(enemy)


def GAME_OVER(fond, enemies):
    for enemy in enemies:
        enemy.y = 7000
    text = fond.render('GAME OVER', True, RED)
    global GAMEOVER
    global game_over_text_done
    GAMEOVER = True
    mixer.music.stop()
    game_over_text_done = text


def restart_game(enemies, event):
    global GAMEOVER
    global life_time
    global score_value
    global music_playing
    if GAMEOVER:
        if event.key == pygame.K_r:
            for enemy in enemies:
                enemies.remove(enemy)
                GAMEOVER = False
                life_time = 5
                score_value = 0
                mixer.music.load('background1.wav')
                mixer.music.play(-1)
                music_playing = 'normal'



def enemy_handle(enemies_alive, player):
    for enemy in enemies_alive:
        if enemy.colliderect(player):
            GAME_OVER(fond, enemies_alive)
        if enemy.x < 10:
            enemy.y += plus
            enemy.x += 10
        if enemy.x > WIDTH - (ENEMY_WIDTH + 10):
            enemy.y += plus
            enemy.x -= 10
        if enemy.x - ENEMY_SPEED > 0 and enemy.y == first or enemy.y == third or enemy.y == fifth or enemy.y == seventh or enemy.y == ninth or enemy.y == eleventh:
            enemy.x -= ENEMY_SPEED
        if enemy.x + ENEMY_SPEED < WIDTH and enemy.y == second or enemy.y == fourth or enemy.y == sixth or enemy.y == eight or enemy.y == tenth:
            enemy.x += ENEMY_SPEED


def score_rendering(value, font, x, y):
    score = font.render("score : " + str(value), True, WHITE)
    WINDOW.blit(score, (x, y))


def life_rendering(life_value, life_fond, x, y):
    try:
        life = life_fond.render('time overs in: ' + str(life_value // 1), True, WHITE)
        WINDOW.blit(life, (x, y))
    except:
        global life_time
        life_time = -1


def screen_display(bullets, player_bullet, player_image, player_rect, enemys_alive, back, mikasa_image, pressed):
    WINDOW.blit(back, (0, 0))
    WINDOW.blit(player_image, (player_rect.x, player_rect.y))
    if enemys_alive != []:
        for enemy in enemys_alive:
            WINDOW.blit(enemy_image, (enemy.x, enemy.y))
    if bullets != []:
        for bullet in bullets:
            WINDOW.blit(player_bullet, (bullet.x, bullet.y))
    score_rendering(score_value, font, score_textX, score_textY)
    restart_texting(restart_fond, restart_X, restart_Y)
    if GAMEOVER:
        WINDOW.blit(game_over_text_done, (overX, overY))
    if not GAMEOVER:
        life_rendering(life_time, fond_life, life_X, life_Y)
    if pressed[pygame.K_h]:
        WINDOW.blit(mikasa_image, (WIDTH//2 - mikasa_width//2, HEIGHT//2 - mikasa_height//2))

    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets_fired) < 3 and not GAMEOVER:
                    bullet_sound.play()
                    bullet = pygame.Rect(player_rect.x + 16, player_rect.y - 32, 32, 32)
                    bullets_fired.append(bullet)
                mikasa_ereh(ereh_sound, event)
                restart_game(enemys_alive, event)
                king_crimson(king_krimson, enemys_alive, event)
                music_changing(music_playing, event)

        global life_time
        if not GAMEOVER:
            life_time -= 0.01
        if life_time < 0:
            GAME_OVER(fond, enemys_alive)

        create_enemys(enemys_alive)

        bullets_and_enemys_handle(bullets_fired, enemys_alive)

        enemy_handle(enemys_alive, player_rect)

        keys_pressed = pygame.key.get_pressed()
        player_movement(player_rect, keys_pressed)

        screen_display(bullets_fired, player_bullet, player_image, player_rect, enemys_alive, background, mikasa, keys_pressed)

    pygame.quit()


if __name__ == "__main__":
    main()
