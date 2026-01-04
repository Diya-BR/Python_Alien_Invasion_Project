from pathlib import Path
class GameStats:
    """Track statistics for Alien invalsion."""
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # High score should never be reset.
        self.path = Path('High_Score.txt')
        self.high_score = int(self.path.read_text())
    
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1