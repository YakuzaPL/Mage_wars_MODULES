import random
import pygame
from pygame import mixer
import game_engine
import hero

# images
WIZARD_IMAGE_LOCATION = "assets/wizard.png"
WAND_IMAGE_LOCATION = "assets/magic-wand.png"
ENEMY_IMAGE_LOCATION = "assets/fortune-teller.png"
SPELL_IMAGE_LOCATION = "assets/flash.png"

# sounds
BACKGROUND_SOUND_LOCATION = "sounds/background.mp3"
SPELL_SOUND_LOCATION = "sounds/spell_sound.wav"
DEATH_SOUND_LOCATION = "sounds/death.wav"

# fonts
MAIN_FONT_LOCATION = "assets/AkayaTelivigala-Regular.ttf"

pygame.init()
clock = pygame.time.Clock()

# background sound
mixer.music.load(BACKGROUND_SOUND_LOCATION)
mixer.music.play(-1)
mixer.music.set_volume(0.3)

score = 0

font = pygame.font.Font(MAIN_FONT_LOCATION, 32)
text_x = 10
text_y = 10

# screen size setting
screen = pygame.display.set_mode((800, 600))

# game title
pygame.display.set_caption('Wizzard Wars')

# game icon
icon = pygame.image.load(WAND_IMAGE_LOCATION)
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load(WIZARD_IMAGE_LOCATION).convert_alpha()
player_position_x = 368
player_position_y = 480
player_speed_x = 0
player_speed_y = 0
player_move_speed = 7

# evil wizard
enemy_img = []
enemy_x = []
enemy_y = []
enemy_speed_x = []
num_of_enemies = 16

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(ENEMY_IMAGE_LOCATION).convert_alpha())
    enemy_x.append(random.randint(1, 735))
    enemy_y.append(0)
    enemy_speed_x.append(random.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6]))

# spell cast
spell_img = pygame.image.load(SPELL_IMAGE_LOCATION).convert_alpha()
spell_x = -50
spell_y = -50
spell_speed_y = 15
spell_state = "ready"  # ready / throw

# end game
over_font = pygame.font.Font(MAIN_FONT_LOCATION, 70)
game_state = "play"  # play / over


def gen_enemy(i):
    global enemy_x, enemy_y, enemy_speed_x
    enemy_x[i] = random.randint(1, 735)
    enemy_y[i] = random.randint(0, 80)
    enemy_speed_x[i] = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])


running = True

while running:
    # background colour
    screen.fill((102, 102, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "play":
                if event.key == pygame.K_SPACE:
                    if spell_state == "ready":
                        throw_sound = mixer.Sound(SPELL_SOUND_LOCATION)
                        throw_sound.play()
                        spell_y = player_position_y
                        spell_x = player_position_x
                        hero.throw_spear(spell_x, spell_y, screen, spell_img)
                        spell_state = "throw"
            if game_state == "over":
                if event.key == pygame.K_r:
                    game_engine.new_game(num_of_enemies, gen_enemy)
                    game_state = "play"
                    score = 0
                    player_position_x = 368
                    player_position_y = 480

    # player movement
    keys = pygame.key.get_pressed()
    player_speed_x = 0
    player_speed_y = 0
    if game_state == "play":
        if keys[pygame.K_LEFT]:
            player_speed_x = - player_move_speed
        elif keys[pygame.K_RIGHT]:
            player_speed_x = player_move_speed

        if keys[pygame.K_UP]:
            player_speed_y = - player_move_speed
        elif keys[pygame.K_DOWN]:
            player_speed_y = player_move_speed

    player_position_x += player_speed_x
    player_position_y += player_speed_y

    # game field restrictions
    if player_position_x <= 0:
        player_position_x = 0
    elif player_position_x >= 736:
        player_position_x = 736

    if player_position_y <= 0:
        player_position_y = 0
    elif player_position_y >= 536:
        player_position_y = 536

    # opponent movement restriction
    for i in range(num_of_enemies):

        if enemy_y[i] > 536:
            game_engine.game_over(over_font, screen, num_of_enemies, enemy_y)
            player_position_y = 2000
            game_state = "over"
            break
        if enemy_x[i] <= 0:
            enemy_speed_x[i] *= -1
            enemy_y[i] += 32
        elif enemy_x[i] >= 736:
            enemy_speed_x[i] *= -1
            enemy_y[i] += 32

        # collision
        collision = game_engine.is_collision(enemy_x[i], enemy_y[i], spell_x, spell_y, 25)
        if collision:
            throw_sound = mixer.Sound(DEATH_SOUND_LOCATION)
            throw_sound.play()
            spell_state = "ready"
            spell_y = -50
            score += 1
            gen_enemy(i)

        player_collision = game_engine.is_collision(enemy_x[i], enemy_y[i], player_position_x, player_position_y, 50)
        if player_collision:
            game_engine.game_over(over_font, screen, num_of_enemies, enemy_y)
            player_position_y = 2000
            game_state = "over"

        game_engine.enemy(enemy_x[i], enemy_y[i], i, screen, enemy_img)

        enemy_x[i] += enemy_speed_x[i]

    if spell_y <= -32:
        spell_y = -50
        spell_state = "ready"

    # thrown spell
    if spell_state == "throw":
        hero.throw_spear(spell_x, spell_y, screen, spell_img)
        spell_state = "throw"
        spell_y -= spell_speed_y

    hero.player(player_position_x, player_position_y, screen, player_img)
    game_engine.show_score(text_x, text_y, font, screen, score)
    pygame.display.update()
    clock.tick(60)
