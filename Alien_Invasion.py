import sys  #tools in the sys module can be used to exit the game when the player quits.
import pygame #The pygame module contains the functionality we need to make a game
import random
from pathlib import Path
from time import sleep
from Settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullets import Bullet
from alien import Alien
# from meteorites import Meteorite

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game resources."""
        pygame.init()  # initializes the background settings that Pygame needs to work properly
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height)) #creates a display window
        pygame.display.set_caption("Alien Invasion")
        
        # Create an instance to store game statistics and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        #self.meteorites = pygame.sprite.Group()
        self.ship=Ship(self)
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.bullet_shot = False
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.last_row_time = pygame.time.get_ticks()
        self.row_delay = 18000  # 60 seconds
        
        '''# Start Alien Invasion in an active state.
        self.game_active = True'''
        
        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Make the Play button.
        self.play_button = Button(self, "Play", -35)
        self.help_button = Button(self, "Help", 35)
        #self.last_meteorite_time = pygame.time.get_ticks()
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
                # self._update_meteorites()
                # self._check_meteorite_spawn()
                
                self._add_new_row_every_few_sec()
                
            self._update_screen()
            self.clock.tick(60)  #The tick() method takes one argument: the frame rate for the game. Using a value of 60, means Pygame will do its best to make the loop run exactly 60 times per second.
            
    def _check_events(self):
        """Respond to keypresses and mouse events."""   
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # when the player clicks the game window’s close button, a pygame.QUIT event is detected.
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif (event.type == pygame.MOUSEBUTTONDOWN) :
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        help_clicked = self.help_button.rect.collidepoint(mouse_pos)
        if play_clicked and not self.game_active:
            self._start_game()
        if help_clicked and not self.game_active:
            self._help_screen_display()
            
    def _start_game(self):
        # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            # RESET THE TIMER HERE
            self.last_row_time = pygame.time.get_ticks()
            # self.last_meteorite_time = pygame.time.get_ticks()
            
            self.game_active = True
            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
    
    def _help_screen_display(self):
        """Display instructions and wait for user to exit."""
        help_active = True
        while help_active:
            self.screen.fill(self.settings.bg_color)
            
            # Read file
            path = Path('help_instructions.txt')
            lines = path.read_text().splitlines() if path.exists() else ["File not found."]

            # Draw Title
            title = self.sb.font.render("GAME INSTRUCTIONS", True, (213, 245, 7))
            self.screen.blit(title, (self.settings.screen_width // 2 - 150, 50))

            # Draw Lines
            y = 150
            for line in lines:
                line_img = self.sb.small_font.render(line, True, (255, 255, 255))
                self.screen.blit(line_img, (100, y))
                y += 35 # Spacing between lines

            # Draw Footer
            footer = self.sb.small_font.render("Press any key to return to Menu", True, (100, 100, 100))
            self.screen.blit(footer, (self.settings.screen_width // 2 - 150, 650))

            pygame.display.flip()

            # Wait for input to close the help screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    help_active = False
                
    
    def _add_new_row_every_few_sec(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_row_time > self.row_delay:
            # Check if the top area is clear before adding
            top_area_clear = True
            for alien in self.aliens:
                # If any alien is higher than two alien heights from the top offset
                if alien.rect.top < (self.settings.ship_top_offset + alien.rect.height * 2):
                    top_area_clear = False
                    break
            
            if top_area_clear:
                self._add_alien_row()
                self.last_row_time = current_time
                
    def _check_keydown_events(self, event):     
        if self.game_active == True:
            """Responds to keypresses."""  
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.ship.moving_right = True
            elif event.key == pygame.K_UP:
                self.ship.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.ship.moving_down = True
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_f:
                self.settings.fullscreen = not self.settings.fullscreen
                self._apply_fullscreen()
            elif (event.key == pygame.K_SPACE) or (event.key == pygame.K_s):
                self.bullet_shot = True
                self._fire_bullet()
        if (event.key == pygame.K_p) and not self.game_active:
            self.game_active = True
            pygame.mouse.set_visible(False)
            
    def _apply_fullscreen(self):
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
 
    def _check_keyup_events(self, event):     
        """Responds to releases."""  
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif (event.key == pygame.K_SPACE) or (event.key == pygame.K_s):
            self.bullet_shot = False
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        current_time = pygame.time.get_ticks()  # ms since pygame started

        if (current_time - self.last_shot_time >= self.settings.bullet_cooldown) and self.bullet_shot and (len(self.bullets) < self.settings.bullets_allowed):
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.last_shot_time = current_time

    def _update_bullets(self):
        """Update position of bullets and get rid  of old bullets."""
        self.bullets.update()
        if self.bullet_shot:
            self._fire_bullet()
                
        # Get rid of bullets that have dissappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Check for anybullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True )
        
        if collisions :
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.ship.center_ship()
            self._create_fleet()
            self.settings.increase_speed()
            
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
        '''    
        # Check if bullets hit meteorites
        meteor_impacts = pygame.sprite.groupcollide(self.bullets, self.meteorites, True, True)
        if meteor_impacts:
            self.stats.score += 60 # Hit reward
            self.sb.prep_score()'''
            
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()
        
        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
               
            
    def _create_fleet(self):
        """Create the fleet"""
        #Create an alien and keep adding aliens until there's no room left
        #Spacing between aliens is one alien width and one alien height.
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, (self.settings.ship_top_offset + (alien_height * 2))
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
        
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet. """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _add_alien_row(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x = alien_width
        y_position = alien_height + self.settings.ship_top_offset
        
        while current_x < (self.settings.screen_width - 2 * alien_width):
            if random.choice([True, False]):
                self._create_alien(current_x, y_position)
            current_x += 2* alien_width
    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            #Decrement ships_lef, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # print(f"DEBUG: Level: {self.stats.level} | Ships Left: {self.stats.ships_left}")
            # Reset movement flags so the ship doesn't move on respawn
            self.ship.moving_right = False
            self.ship.moving_left = False
            self.ship.moving_up = False
            self.ship.moving_down = False
            
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            
            #Pause.
            sleep(0.5)
        else:
            self.game_active = False
            # self._draw_game_over_msg()
            pygame.mouse.set_visible(True)
    
    def _draw_game_over_msg(self):
        """Draw 'GAME OVER' below the Play button."""
        msg = "GAME OVER"
        # Using your 'large_font' for a dramatic effect
        over_image = self.sb.large_font.render(msg, True, (255, 0, 0))
        over_rect = over_image.get_rect()
        
        # Position it 100 pixels below the Play Button
        over_rect.centerx = self.play_button.rect.centerx
        over_rect.top = self.play_button.rect.bottom + 100
        
        self.screen.blit(over_image, over_rect)
    
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_aliens_bottom(self):
        """Check if any aliens have bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom > self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    def _add_new_row_every_few_sec(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_row_time > self.row_delay:
            alien_sample = Alien(self)
            spawn_zone_limit = alien_sample.rect.height * 3 + self.settings.ship_top_offset
            # Check if any current alien is still in the way
            space_is_clear = True
            for alien in self.aliens.sprites():
                if alien.rect.top < spawn_zone_limit:
                    space_is_clear = False
                    break
            if space_is_clear:
                self._add_alien_row()
                self.last_row_time = current_time
    
    '''def _check_meteorite_spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_meteorite_time > 20000:
            new_meteorite = Meteorite(self)
            self.meteorites.add(new_meteorite)
            self.last_meteorite_time = current_time
    
    def _update_meteorites(self):
        self.meteorites.update()
        
        # Check for collision with ship
        if pygame.sprite.spritecollideany(self.ship, self.meteorites):
            self._ship_hit()
            
        # Check for meteorites that were dodged (Big Bonus!)
        for meteorite in self.meteorites.copy():
            if meteorite.rect.top > self.settings.screen_height:
                self.meteorites.remove(meteorite)
                self.stats.score += 250  #Dodge reward
                self.sb.prep_score()
                self.sb.check_high_score()
    '''
    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        # self.meteorites.draw(self.screen)
        # Draw the score information.
        self.sb.show_score()
        
        # Draw the play button if the game is inactive.
        if not self.game_active:
            self._dim_screen()
        
            # Check if this is a "Game Over" state or just the "Start" state
            if self.stats.ships_left == 0:
                self._draw_game_over_msg()
                
            self.play_button.draw_button()
            self.help_button.draw_button()
        
        # Make the most recently drawn screen visible.
        pygame.display.flip() #tells Pygame to make the most recently drawn screen visible.
        # If the player has no ships left, show Game Over
    
    def _dim_screen(self):
        """Draw a semi-transparent black overlay over the entire screen."""
        # Create a surface the size of the screen
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(150)  # 0 is invisible, 255 is fully opaque
        overlay.fill((0, 0, 0)) # Black color
        self.screen.blit(overlay, (0, 0))
        
    def _draw_game_over_msg(self):
        """Draw 'GAME OVER' below the Play button."""
        msg = "GAME OVER"
        # Using your 'large_font' for a dramatic effect
        over_image = self.sb.large_font.render(msg, True, (255, 0, 0))
        over_rect = over_image.get_rect()
        
        # Position it 100 pixels below the Play Button
        over_rect.centerx = self.play_button.rect.centerx
        over_rect.top = self.play_button.rect.bottom + 100
        
        self.screen.blit(over_image, over_rect)
    
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
            