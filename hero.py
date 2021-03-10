def player(x, y, screen, player_img):
    screen.blit(player_img, (x, y))


def throw_spear(x, y, screen, spell_img):
    screen.blit(spell_img, (x + 16, y + 10))
