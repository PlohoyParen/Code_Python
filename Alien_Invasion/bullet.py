import pygame as pg
from pygame.sprite import Sprite 

class Bullet(Sprite):
    
    def __init__(self, ai_settings, screen, ship):
        
        super().__init__()
        self.screen = screen
        
        #creat a bullet at (0,0)). Just draw a few rects.
        self.image = pg.image.load('image/fire13.png')
        self.image = pg.transform.scale(self.image, (1000, 10))
        self.rect = self.image.get_rect()
        #self.rect = pg.Rect(0, 0, ai_settings.bullet_width, 
        #                    ai_settings.bullet_height)
        #place the bullet on the top of ship
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        #store current bullet location
        self.y = float(self.rect.y)
        
        self.speed_factor = ai_settings.bullet_speed_factor
        #self.color = ai_settings.bullet_color

    def update(self):
        """ Updates current bullet location """
        self.y -= self.speed_factor
        self.rect.y = self.y

    def blitme(self):
       self.screen.blit(self.image, self.rect)