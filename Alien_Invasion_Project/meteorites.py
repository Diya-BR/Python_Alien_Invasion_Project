import pygame
import random
from pygame.sprite import Sprite

class Meteorite(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load('images/Meteorite.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect()
        
        #Start at a random X position at the top
        self.rect.x = random.randint(0, self.settings.screen_width - self.rect.width)
        self.rect.bottom = 0  # Just above the screen
        
        self.y = float(self.rect.y)
        self.speed = 4.5  #Slightly faster than aliens
        
    def update(self):
        """Move the meteorite down the screen."""
        self.rect.y += self.speed
        self.rect.y = self.y
        