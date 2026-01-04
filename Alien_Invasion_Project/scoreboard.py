import pygame.font
from pygame.sprite import Group
from pathlib import Path
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""
    
    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.path = Path('High_Score.txt')
        # Font settings for scoring information.
        self.text_color = (240, 240, 245)
        self.high_score_color = (213, 245, 7)
        # Main score font
        self.font = pygame.font.SysFont(None, 36)
        
        # Smaller font for the Level
        self.small_font = pygame.font.SysFont(None, 26)
        
        # Larger font for the High Score
        self.large_font = pygame.font.SysFont(None, 42)
        
        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    
       
        
    def prep_score(self):
        """Turn the score into a rendered image."""
        round_score = round(self.stats.score, -1) #tells Python to round the value of stats.score to the nearest 10 and assign it to rounded_score.
        score_str = f"Score: {round_score:,}"
        
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        
        #Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """Draw scores, levels and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        
        high_score_str = f"{high_score}"
        self.path.write_text(high_score_str)
        self.high_score_image = self.large_font.render(f'H_Score: ' + f"{high_score:,}", True, self.high_score_color, self.settings.bg_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def check_high_score(self):
        """Check to see if there's a new high score."""
        
        self.stats.high_score = int(self.path.read_text())
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
        
    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.stats.level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5
        
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game, 49, 50)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)