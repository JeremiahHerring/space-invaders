import pygame as pg
from vector import Vector
from point import Point
from laser import Laser 
from time import sleep
from pygame.sprite import Sprite
from timer import Timer

class Ship(Sprite):
    def __init__(self, ai_game, v=Vector()):
        super().__init__()
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.stats = ai_game.stats
        self.sb = None

        self.original_image = pg.image.load('images/ship.png') 
        self.image = self.original_image  
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        scr_r = self.screen_rect 
        self.x = float(scr_r.midbottom[0])
        self.y = float(scr_r.height)
        self.v = v
        self.lasers = pg.sprite.Group()
        self.firing = False
        self.last_shot_time = 0
        self.fire_cooldown = 300
        self.fleet = None

        self.explosion_images = [pg.image.load(f"images/ship_boom{n}.png") for n in range(3)]
        self.explosion_timer = Timer(images=self.explosion_images, delta=100, loop_continuously=False, running=False)
        self.is_exploding = False
        self.explosion_position = None  

        self.is_vulnerable = False
        self.is_vulnerable_timer = 0
        self.is_vulnerable_interval = 1000

    def set_fleet(self, fleet): 
        self.fleet = fleet 

    def set_sb(self, sb): 
        self.sb = sb

    def reset_ship(self):
        self.lasers.empty()
        self.center_ship()
        self.v = Vector(0, 0)

    def center_ship(self):         
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def bound(self):
        x, y, scr_r = self.x, self.y, self.screen_rect
        self.x = max(0, min(x, scr_r.width - self.rect.width)) 
        self.y = max(0, min(y, scr_r.height - self.rect.height))

    def ship_hit(self):
        """Handle ship being hit by an alien."""
        if self.is_vulnerable:
            return
        
        self.stats.ships_left -= 1
        print(f"Only {self.stats.ships_left} ships left now")
        
        self.sb.prep_ships()
        if self.stats.ships_left <= 0:
            self.stats.update_high_score()
            self.ai_game.game_over()

        self.is_exploding = True
        self.is_vulnerable = True
        self.is_vulnerable_timer = pg.time.get_ticks()
        self.explosion_position = (self.x, self.y) 
        self.explosion_timer.start()

        self.lasers.empty()
        #self.fleet.aliens.empty()

    def fire_laser(self):
        current_time = pg.time.get_ticks()

        if current_time - self.last_shot_time > self.fire_cooldown:
            if len(self.lasers) < self.settings.lasers_allowed:
                left_laser = Laser(self.ai_game, side="left")   
                right_laser = Laser(self.ai_game, side="right") 
                self.lasers.add(left_laser, right_laser)  
                
                self.last_shot_time = current_time 
        
    def open_fire(self): 
        self.firing = True 

    def cease_fire(self): 
        self.firing = False

    def update(self):
        if self.is_vulnerable:
            current_time = pg.time.get_ticks()
            if current_time - self.is_vulnerable_timer > self.is_vulnerable_interval:
                self.is_vulnerable = False

        if self.is_exploding:
            if self.explosion_timer.finished():
                self.is_exploding = False
                self.explosion_timer.reset()
                self.image = self.original_image 
                self.center_ship() 
            else:
                self.image = self.explosion_timer.current_image()
        else:
            self.x += self.v.x 
            self.y += self.v.y
            self.bound()

        if self.firing:
            self.fire_laser()
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)
        for laser in self.lasers.sprites():
            laser.draw() 
        self.draw()

    def draw(self): 
        if self.is_exploding:
            self.rect.x, self.rect.y = self.explosion_position
        else:
            self.rect.x, self.rect.y = self.x, self.y
        self.screen.blit(self.image, self.rect)

def main():
    print('\n*** message from ship.py --- run from alien_invasions.py\n')

if __name__ == "__main__":
    main()