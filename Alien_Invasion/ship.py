import pygame as pg

class Ship():
   def __init__(self, ai_settings, screen):
        self.screen = screen
        self.ai_settings = ai_settings
        
        #load the image of main ship
        self.image = pg.image.load('image\ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        #place ship at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #movement control flags
        self.moving_right = False
        self.moving_left = False
        
        #speed control
        self.center = float(self.rect.centerx)
        
   def blitme(self):
       self.screen.blit(self.image, self.rect)

   def update(self):
       """ updates ship position each cycle """
       if self.moving_right and self.rect.right < self.screen_rect.right:
           self.center += self.ai_settings.ship_speed_factor 
       if self.moving_left and self.rect.left > 0:
           self.center -= self.ai_settings.ship_speed_factor 
       
       #updates rect postion
       self.rect.centerx = self.center
       
   def center_ship(self):
       self.center = self.screen_rect.centerx
       
#self.rect - surface for image of a ship
#self.screen_rect - rect size of the main screen
#'self.rect' works with int only, so 'self.rect.centerx = self.center' let to 
#wortk w/ floats and then pass it to '.rect'       