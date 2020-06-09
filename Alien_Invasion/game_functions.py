import pygame as pg
import sys
# created modules
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ manages key press """
    # moving ship left and right
    if event.key == pg.K_RIGHT:
        ship.moving_right = True
    if event.key == pg.K_LEFT:
        ship.moving_left = True
    # bullets - press space
    if event.key == pg.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # exit the game
    if event.key == pg.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """ manages key release """
    if event.key == pg.K_RIGHT:
        ship.moving_right = False
    if event.key == pg.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, stats, screen, ship, bullets, aliens, play_button, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pg.mouse.set_visible(False)
        stats.game_active = True
        stats.reset_stats()
        bullets.empty()
        aliens.empty()
        # new attempt
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)


def check_events(ai_settings, stats, screen, ship, bullets, aliens, play_button):
    """    manages events - key and mouse actions    """

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            check_play_button(ai_settings, stats, screen, ship,
                              bullets, aliens, play_button, mouse_x, mouse_y)

        elif event.type == pg.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pg.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button):
    """    updates the screen    """
    screen.fill(ai_settings.bg_color)

    ship.blitme()
    aliens.draw(screen)

    # drawing bullets
    for bullet in bullets.sprites():
        bullet.blitme()

    if not stats.game_active:
        play_button.draw_buttom()

    pg.display.flip()

############################################################################
######################  Bullet functions  ##################################
############################################################################


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """ manages bullets """
    bullets.update()
    # removing bullets that are gone off screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pg.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """ fires a bullet is allowed """
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

############################################################################
######################  Alien fleet functions  #############################
############################################################################


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # check ship - any of aliens collision
    if pg.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    # check if alien is at the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    # aleins in one row (along x)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x

    # rows of aliens (along y)
    alien_height = alien.rect.height
    alien.rect.y = alien_height + 2*alien_height*row_number

    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # creats an instance of an alien and add it to the row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_diraction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # if alien is at the bottom of the screen, treat it like a ship hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

################# Auxiliary functions #################


def get_number_aliens_x(ai_settings, alien_width):
    """ calculation for size of an alien fleet """
    avalible_space_x = ai_settings.width - (2*alien_width)
    number_aliens_x = int(avalible_space_x/(2*alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    avalible_space_y = ai_settings.height - ship_height - 3*alien_height
    number_rows = int(avalible_space_y/(2*alien_height))
    return number_rows

############################################################################
####################  Statiscts, end and restart  ##########################
############################################################################


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    # take one life
    stats.ships_left -= 1
    if stats.ships_left > 0:
        # restart the new attempt
        bullets.empty()
        aliens.empty()
        # new attempt
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)
    else:
        pg.mouse.set_visible(True)
        stats.game_active = False
