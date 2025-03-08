import pygame as pg
from vector import Vector
from alien import Alien, UFO
from pygame.sprite import Sprite
from timer import Timer
from random import randint

class Fleet(Sprite):
    def __init__(self, ai_game): 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.aliens = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb
        self.v = Vector(self.settings.alien_speed, 0)

        self.spacing = 1.2 
        self.margin = 50
        self.create_fleet()

        self.ufo_timer = 0
        self.ufo_interval = randint(500, 800)

    def reset_fleet(self):
        self.aliens.empty()
        self.create_fleet()

    def create_fleet(self):
        """Creates a fleet of aliens with 6 rows, ensuring proper alignment."""
        alien = Alien(ai_game=self.ai_game, v=self.v)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        num_columns = int((self.settings.scr_width - 2 * self.margin) // (alien_width * self.spacing))
        num_rows = 6 

        start_x = (self.settings.scr_width - (num_columns * alien_width * self.spacing)) // 2
        start_y = 150

        for row in range(num_rows):
            alien_type = 2 if row < 2 else 1 if row < 4 else 0  
            y_position = start_y + row * (alien_height * self.spacing)
            self.create_row(y_position, num_columns, alien_type, start_x)

    def create_row(self, y, num_columns, alien_type, start_x):
        """Creates a single row of aliens at a given y position."""
        for col in range(num_columns):
            x_position = start_x + col * (Alien.alien_images[0][0].get_width() * self.spacing)
            new_alien = Alien(self.ai_game, v=self.v)
            new_alien.timer = Timer(images=Alien.alien_images[alien_type], delta=1000, start_index=alien_type % 2)
            new_alien.rect.y = y
            new_alien.y = y
            new_alien.x = x_position
            new_alien.rect.x = x_position
            self.aliens.add(new_alien)

    def check_edges(self):
        for alien in self.aliens:
            if alien.check_edges(): 
                return True 
        return False

    def check_bottom(self):
        for alien in self.aliens:
            if alien.rect.bottom >= self.settings.scr_height:
                self.ship.ship_hit()
                return True
        return False

    def update(self): 
        collisions = pg.sprite.groupcollide(self.ship.lasers, self.aliens, True, False)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score() 
                self.sb.check_high_score()
                for alien in aliens:
                    alien.hit()

        ufo_collisions = pg.sprite.groupcollide(self.ship.lasers, self.ufos, True, False)
        
        if ufo_collisions:
            self.stats.score += self.settings.ufo_points
            for ufos in ufo_collisions.values():
                self.stats.score += self.settings.ufo_points * len(ufos)
                self.sb.prep_score()
                self.sb.check_high_score()
                for ufo in ufos:
                    ufo.hit()
        
        if not self.ship.is_vulnerable:
            if pg.sprite.spritecollideany(self.ship, self.aliens):
                print("Ship hit!")
                self.ship.ship_hit()
                return

            if pg.sprite.spritecollideany(self.ship, self.ufos):
                print("Ship hit by UFO!")
                self.ship.ship_hit()
                return

        if not self.aliens and self.ai_game.game_active:
            self.ship.lasers.empty()
            self.create_fleet()
            self.stats.level += 1
            self.sb.prep_level()
            return
        
        if self.check_bottom():
            return 
        
        if self.check_edges():
            self.v.x *= -1 
            for alien in self.aliens:
                alien.v.x = self.v.x
                alien.y += self.settings.fleet_drop_speed
            
        for alien in self.aliens:
            alien.update()

        self.ufos.update()

        self.ufo_timer += 1
        if self.ufo_timer >= self.ufo_interval:
            self.spawn_ufo()
            self.ufo_timer = 0
            self.ufo_interval = randint(500, 800)
        
    def spawn_ufo(self):
        new_ufo = UFO(self.ai_game)
        self.ufos.add(new_ufo)

    def draw(self): 
        for alien in self.aliens:
            alien.draw()
        for ufo in self.ufos:
            ufo.draw()