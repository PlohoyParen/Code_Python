import pygame as pg
from pygame.sprite import Sprite


class Alien(Sprite):
    """ class for a single alient, that will be used for the whole fleet """

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # load enemy image and get its dimentions
        self.image = pg.image.load('image\enemyBlack2.png')
        self.rect = self.image.get_rect()
        # current x, y (when enemy is created) are the left upper corner
        # x, y manages current position of an enemy ship
        self.x = self.rect.x
        self.y = self.rect.y

    def blitme(self):
        """ method that draws an alien """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """ return True if alien is at the edge of the screen """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right - self.rect.width/2:
            return True
        elif self.rect.x <= self.rect.width/2:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_diraction)
        self.rect.x = self.x
