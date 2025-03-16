import pygame as pg
from pygame.sprite import Sprite, Group

BARRIER_ARCH_HEIGHT = 4 
BARRIER_ARCH_WIDTH_2 = 4  
BARRIER_WIDTH = 150
BARRIER_HEIGHT = 80

class BarrierPiece(Sprite):
    def __init__(self, ai_game, rect):
        super().__init__()
        self.screen = ai_game.screen
        self.rect = rect
        self.color = (0, 255, 0)  
        self.health = 1 
    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()  
            
    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)

class Barrier(Sprite):
    def __init__(self, ai_game, width, height, deltax, deltay, x, y):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.deltax, self.deltay = deltax, deltay
        self.settings = ai_game.settings
        self.ship_lasers = ai_game.ship.lasers
        self.fleet = ai_game.fleet
        self.fleet_lasers = ai_game.fleet.fleet_lasers
        self.barrier_pieces = Group()
        self.create_barrier_pieces()
    
    def create_barrier_pieces(self):
        left, top = 0, 0
        height, width = int(self.height/self.deltay), int(self.width/self.deltax)
        for i in range(height):
            for j in range(width):
                rect = pg.Rect(self.x + left + j * self.deltax,
                               self.y + top + i * self.deltay,
                               self.deltax, self.deltay)
                
                if height - i < BARRIER_ARCH_HEIGHT and abs(j - width/2) < BARRIER_ARCH_WIDTH_2:
                    continue    
                
                self.barrier_pieces.add(BarrierPiece(ai_game=self.ai_game, rect=rect))
    
    def reset(self):
        self.barrier_pieces.empty()
        self.create_barrier_pieces()
    
    def update(self):
        alien_collisions = pg.sprite.groupcollide(self.barrier_pieces, self.fleet_lasers, False, True)
        for barrier_piece in alien_collisions:
            barrier_piece.hit()
        
        ship_collisions = pg.sprite.groupcollide(self.barrier_pieces, self.ship_lasers, False, True)
        for barrier_piece in ship_collisions:
            barrier_piece.hit()
        
        self.draw()
    
    def draw(self):
        for barrier_piece in self.barrier_pieces:
            barrier_piece.draw()

class Barriers:

    positions = [(BARRIER_WIDTH * x + BARRIER_WIDTH / 2.0, 600) for x in range(0, 7, 2)]
    
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.barriers = Group()
        self.create_barriers()
    
    def create_barriers(self):
        width = self.settings.scr_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.scr_height - 2.1 * height
        
        barriers = [Barrier(ai_game=self.ai_game,
                            width=BARRIER_WIDTH, height=BARRIER_HEIGHT,
                            deltax=10, deltay=10,
                            x=x, y=y) for x, y in Barriers.positions]
        
        for barrier in barriers:
            self.barriers.add(barrier)
    
    def reset(self):
        for barrier in self.barriers:
            barrier.reset()
    
    def update(self):
        for barrier in self.barriers:
            barrier.update()
    
    def draw(self):
        for barrier in self.barriers:
            barrier.draw()