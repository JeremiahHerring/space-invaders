import sys
import pygame as pg
from colors import OFF_WHITE, DARK_GREY
from settings import Settings
from ship import Ship
from vector import Vector
from alien import Alien
from fleet import Fleet
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from event import Event
from start_screen import StartScreen
from death_screen import DeathScreen
from barrier import Barriers

class AlienInvasion:
    # di = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
    #       pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1),
    #       pg.K_d: Vector(1, 0), pg.K_a: Vector(-1, 0),
    #       pg.K_w: Vector(0, -1), pg.K_s: Vector(0, 1)}
    def __init__(self):
        pg.init()   
        self.clock = pg.time.Clock()
        self.settings = Settings()
        self.screen = pg.display.set_mode(self.settings.w_h)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.points_texts = []
        self.ship = Ship(ai_game=self)
        self.fleet = Fleet(ai_game=self)
        self.ship.set_fleet(self.fleet)
        self.ship.set_sb(self.sb)
        self.barriers = Barriers(ai_game=self)


        pg.display.set_caption("Alien Invasion")
        self.bg_color = self.settings.bg_color

        self.game_active = False
        self.first = True

        self.play_button = Button(self, "Play")
        self.event = Event(self)

        self.death_screen = DeathScreen(self)

    def game_over(self):
        # self.restart_game()
        self.stats.update_high_score()
        self.game_active = False
        self.death_screen_active = True
        pg.mouse.set_visible(True)

    def reset_game(self):
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.game_active = True

        self.ship.reset_ship()
        self.fleet.reset_fleet()
        self.fleet.reset_lasers()  

    def restart_game(self):
        self.game_active = False
        self.first = True
        self.stats.reset_stats()
        self.sb.prep_score_level_ships()
        self.ship.reset_ship()
        self.fleet.reset_fleet()
        self.fleet.reset_lasers()  

        pg.event.clear()
        self.death_screen_active = False
        pg.mouse.set_visible(False)
        self.game_active = True

    def update_points_texts(self):
        current_time = pg.time.get_ticks()
        for points_text, position, display_time in self.points_texts[:]:
            if current_time - display_time < 1000:
                self.screen.blit(points_text, position)
            else:
                self.points_texts.remove((points_text, position, display_time))

    def run_game(self):
            self.finished = False
            self.first = True
            self.game_active = False
            self.death_screen_active = False

            start_screen = StartScreen(self)
            start_screen.run()

            while not self.finished:
                self.finished = self.event.check_events()
                if self.first or self.game_active:
                    self.first = False
                    self.screen.fill(self.bg_color)
                    self.ship.update()
                    self.fleet.update()
                    self.sb.show_score()
                    self.update_points_texts()
                    self.barriers.update()


                elif self.death_screen_active:
                    result = self.death_screen.run()
                    if result == "play_again":
                        self.death_screen_active = False
                        self.restart_game()
                    elif result == "quit":
                        self.finished = True
                else:
                    self.play_button.draw_button()

                pg.display.flip()
                self.clock.tick(60)
            pg.quit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
