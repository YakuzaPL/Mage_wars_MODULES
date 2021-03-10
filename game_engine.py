import math


def new_game(num_of_enemies, gen_enemy):
    for i in range(num_of_enemies):
        gen_enemy(i)


def game_over(over_font, screen, num_of_enemies, enemy_y):
    for j in range(num_of_enemies):
        enemy_y[j] = 2000
    over_text = over_font.render("GAME OVER!", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def show_score(x, y, font, screen, score):
    score_text = font.render("Wynik: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (x, y))


def is_collision(enemy_x, enemy_y, spear_x, spear_y, d):
    distance = math.sqrt((math.pow(enemy_x - spear_x, 2) + (math.pow(enemy_y - spear_y, 2))))
    if distance < d:
        return True
    else:
        return False


def enemy(x, y, i, screen, enemy_img):
    screen.blit(enemy_img[i], (x, y))
