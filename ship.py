import pygame
from pygame.sprite import Sprite
from Settings import Settings 

class Ship(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game, ship_height = 75, ship_width = 74):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        #Load the ship image and get its rect.
        self.image= pygame.image.load('images/SpaceShip.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (ship_width, ship_height))
        self.rect=self.image.get_rect()
        
        # Start each new ship at the bottom centre of the screen.
        self.rect.midbottom=self.screen_rect.midbottom
        
        #Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        self.y =float(self.rect.y)
        # print(self.x)
        #print(self.y)
        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:  #The code self.rect.right returns the x-coordinate of the right edge of the ship’s rect. 
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x-= self.settings.ship_speed
        if self.moving_up and self.rect.top > (self.screen_rect.top + 100) :
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y+= self.settings.ship_speed
        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y
        
    def center_ship(self):
        """Center the ship on the screen"""
        # Reset the rect position
        self.rect.midbottom = self.screen_rect.midbottom
        
        # IMPORTANT: Reset the decimal coordinates to match the new rect position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image , self.rect)