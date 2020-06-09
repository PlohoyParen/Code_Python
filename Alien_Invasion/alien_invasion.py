import pygame as pg
from pygame.sprite import Group
#created modules
from ship import Ship
import game_functions as gf

from settings import Settings
from game_stats import GameStats
from button import Button

def run_game():
##set screen 
    pg.init()
    ai_settings = Settings()
    screen = pg.display.set_mode((ai_settings.width, ai_settings.height))
    pg.display.set_caption('Alien Invasion')
    
    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, 'New Game')
    ship = Ship(ai_settings, screen)
    
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:
        #always runs to check the key events       
        gf.check_events(ai_settings, stats, screen, ship, bullets, aliens, play_button)
        #runs only when player has some lifes left
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_screen(ai_settings, stats, screen, ship, aliens, bullets, play_button)

run_game()