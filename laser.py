import pygame as pg
from pygame.sprite import Sprite
from random import choice

class Laser(Sprite):
    def __init__(self, ai_game, side="center"):
        """Initialize the laser at the given position on the ship."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ship = ai_game.ship
        self.laser_images = [pg.image.load('other_images/laser_0.png'),
                             pg.image.load('other_images/laser_1.png'),
                             pg.image.load('other_images/laser_2.png'),
                             pg.image.load('other_images/laser_3.png')]

        self.image = choice(self.laser_images)  # Random laser image
        self.rect = self.image.get_rect()

        # Positioning the laser based on the side parameter
        if side == "left":
            self.rect.midtop = ai_game.ship.rect.midleft  # Left side of ship
        elif side == "right":
            self.rect.midtop = ai_game.ship.rect.midright  # Right side of ship
        else:
            self.rect.midtop = ai_game.ship.rect.midtop  # Centered laser

        self.y = float(self.rect.y)  # Store as float for smooth movement

    def update(self):
        """Move the laser upward."""
        self.y -= self.settings.laser_speed  # Move up
        self.rect.y = self.y  # Update position

        # Remove the laser if it moves off-screen
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        """Draw the laser on the screen."""
        self.screen.blit(self.image, self.rect)

class AlienLaser(Sprite):
    def __init__(self, ai_game, position, side="center"):
        """Initialize the laser at the given position on the ship."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.laser_images = [pg.image.load('other_images/laser_0.png'),
                             pg.image.load('other_images/laser_1.png'),
                             pg.image.load('other_images/laser_2.png'),
                             pg.image.load('other_images/laser_3.png')]

        self.image = choice(self.laser_images)  # Random laser image
        self.rect = self.image.get_rect()

        if side == "left":
            self.rect.midtop = (position[0] - self.rect.width // 2, position[1])  # Left side of alien
        elif side == "right":
            self.rect.midtop = (position[0] + self.rect.width // 2, position[1])  # Right side of alien
        else:
            self.rect.midtop = position

        self.y = float(self.rect.y)  # Store as float for smooth movement

    def update(self):
        """Move the laser upward."""
        self.y += self.settings.laser_speed  
        self.rect.y = self.y  # Update position

        if self.rect.top < 0:
            self.kill()

    def draw(self):
        """Draw the laser on the screen."""
        self.screen.blit(self.image, self.rect)
