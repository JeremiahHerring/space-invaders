import pygame as pg
from vector import Vector
from point import Point
from laser import AlienLaser 
from pygame.sprite import Sprite
from timer import Timer
from random import randint
import random
class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien0{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien1{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien2{n}.png") for n in range(2)]

    alien_images = [alien_images0, alien_images1, alien_images2]
    alien_boom = [pg.image.load(f"images/explode{n}.png") for n in range(8)]

    def __init__(self, ai_game, v): 
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.v = v
        self.is_dying = False
        self.is_dead = False

        self.lasers = pg.sprite.Group()
        self.last_shot_time = random.randint(0, 30000)  # Random initial shot time between 0 and 5 seconds
        self.firing_delay = random.randint(0, 30000) 

        type = randint(0, 2)
        self.timer = Timer(images=Alien.alien_images[type], delta=1000, start_index=type % 2)
        self.explosion_timer = Timer(images=Alien.alien_boom, delta=100, loop_continuously=False, running=False)
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
    def reset_lasers(self):
        """Reset the alien's lasers by emptying the laser group."""
        self.lasers.empty() 
    def hit(self):
        if not self.is_dying:
            #print('ALIEN HIT! Alien is dying')
            self.is_dying = True
            self.timer = self.explosion_timer
            self.timer.start()


    def fire_laser(self):
        current_time = pg.time.get_ticks()

        if current_time - self.last_shot_time > self.firing_delay:
            laser = AlienLaser(self.ai_game, self.rect.midtop)  # Use the alien's position for the laser
            self.lasers.add(laser)
            self.ai_game.fleet.fleet_lasers.add(laser)
            self.last_shot_time = current_time 
            
            self.firing_delay = random.randint(0, 30000)
            # DELAYS ALIEN FIRING BETWEEN 0 and 30 sec.
    
    def check_edges(self):
        sr = self.screen.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        r = self.rect 
        return self.x + self.rect.width >= sr.right or self.x <= 0

    def update(self):
        if self.is_dead: return
        if self.is_dying and self.explosion_timer.finished():
            self.is_dying = False
            self.is_dead = True
            #print('Alien is dead')
            self.kill()
            return

        self.x += self.v.x
        self.y += self.v.y
        self.image = self.timer.current_image()

        
        self.fire_laser()
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.top <= 0:
                self.lasers.remove(laser)
        for laser in self.lasers.sprites():
            laser.draw() 
        self.draw()

    def draw(self): 
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)

class UFO(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.is_dying = False
        self.is_dead = False

        self.image = pg.image.load("images/ufo.png")
        self.rect = self.image.get_rect()

        self.direction = randint(0, 1) 
        if self.direction == 0:
            self.rect.x = -self.rect.width
            self.vx = self.settings.ufo_speed 
        else:
            self.rect.x = self.settings.scr_width 
            self.vx = -self.settings.ufo_speed 
        
        self.rect.y = 80 
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.points_display_time = 0  
        self.points_text = None  

    def hit(self):
        if not self.is_dying:
            #print("UFO HIT! Displaying random score.")
            self.is_dying = True
            self.ufo_points = randint(500, 5000)
            self.ai_game.stats.score += self.ufo_points
            self.ai_game.sb.prep_score() 
            self.ai_game.sb.check_high_score()  
            
            font = pg.font.Font("fonts/space.otf", 24)
            points_text = font.render(f"+{self.ufo_points}", True, (255, 255, 0))
            self.points_display_time = pg.time.get_ticks() 

            self.ai_game.points_texts.append((points_text, (self.rect.x, self.rect.y), self.points_display_time))
            self.is_dead = True
            self.kill()

    def update(self):
        if self.is_dead:
            return

        if self.is_dying:
            if pg.time.get_ticks() - self.points_display_time >= 1000:  # 1000ms = 1 second
                self.is_dead = True
                self.kill()
        else:
            self.x += self.vx  
            self.rect.x = self.x

            if (self.direction == 0 and self.rect.left > self.settings.scr_width) or \
               (self.direction == 1 and self.rect.right < 0):
                self.kill()

        # Draw the points if needed
        if self.points_text and pg.time.get_ticks() - self.points_display_time < 1000:
            self.screen.blit(self.points_text, (self.rect.x, self.rect.y))
        
        self.draw()

    def draw(self):
        """Draw the UFO on the screen."""
        if not self.is_dead:
            self.screen.blit(self.image, self.rect)


def main():
    print('\n run from alien_invasions.py\n')

if __name__ == "__main__":
    main()


