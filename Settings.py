import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""
    
    def __init__(self):
        """Initialize the game's static settings. """
        # Screen settings
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (5, 5, 5)
        
        # Ship settings
        
        self.fullscreen = False
        self.ship_top_offset = 15
        self.ship_width = 74
        self.ship_heigt = 75
        
        # Bullet settings
        
        self.bullet_width = 3
        
        self.bullet_height = 15
        #self.bullet_color = (232, 100, 190)
        #self.bullet_color = (17, 76, 171)
        self.bullet_color = (22, 17, 171)
        self.bullet_cooldown = 200  # milliseconds (0.3 seconds)
        self.bullets_allowed = 10
        self.ship_limit = 3 
        
        # Alien settings
        self.fleet_drop_speed = 10
        
        
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        self.ship_speed = 2
        self.alien_speed = 1.0
        self.bullet_speed = 2.5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        
        # Scoring settings
        self.alien_points = 50
        
    def increase_speed(self):
        """increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
        
        

        
