class Settings():
    """Class that stores all the game settings"""
    
    def __init__(self):
        #screen settings
        self.width =  1200
        self.height =  800 
        self.bg_color = (220, 220, 220)
        
        #ship settings
        self.ship_speed_factor = 1.5
        self.ships_limit = 3
        
        #bullet settings
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        #self.bullet_color = (60, 60, 60)
        #num of bullets on the screen allowed
        self.bullets_allowed = 5
        
        #alien setteings
        self.alien_speed_factor = 5 #1
        self.fleet_drop_speed = 50 #20
        self.fleet_diraction = 1 # 1 goes right, -1 goes left