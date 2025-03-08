import pygame as pg
import sys
from button import Button
from game_stats import GameStats

class StartScreen:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.screen_rect = self.screen.get_rect()
        self.bg_color = self.settings.bg_color

        self.alien_images = [
            pg.image.load("images/alien00.png"),
            pg.image.load("images/alien10.png"),
            pg.image.load("images/alien20.png"),
            pg.image.load("images/ufo.png")
        ]
        self.alien_points = [50, 100, 150, "???"]

        self.high_scores = self.load_high_scores()

        self.play_button = Button(self, "Play Game", center=(self.screen_rect.centerx, 700))
        self.high_scores_button = Button(self, "High Scores", center=(self.screen_rect.centerx, 600))

    def load_high_scores(self):
        try:
            with open("high_scores.txt", "r") as file:
                return [int(score.strip()) for score in file.readlines()]
        except FileNotFoundError:
            return []

    def save_high_scores(self):
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores:
                file.write(f"{score}\n")

    def draw_alien_info(self):
        font = pg.font.SysFont(None, 48)
        x = self.screen_rect.centerx - 200
        y = 150
        for i, (image, points) in enumerate(zip(self.alien_images, self.alien_points)):
            self.screen.blit(image, (x, y + i * 100))
            points_text = font.render(f"= {points} points", True, (255, 255, 255))
            self.screen.blit(points_text, (x + 100, y + i * 100 + 20))

    def draw_high_scores(self):
        font = pg.font.SysFont(None, 48)
        high_scores_text = font.render("High Scores:", True, (255, 255, 255))
        self.screen.blit(high_scores_text, (self.screen_rect.centerx - 100, 150))

        y = 200
        for i, score in enumerate(self.high_scores):
            score_text = font.render(f"{i + 1}. {score}", True, (255, 255, 255))
            self.screen.blit(score_text, (self.screen_rect.centerx - 100, y + i * 50))

    def run(self):
        while True:
            self.screen.fill(self.bg_color)

            title_font = pg.font.SysFont(None, 72)
            title_text = title_font.render("Alien Invasion", True, (255, 255, 255))
            self.screen.blit(title_text, (self.screen_rect.centerx - 150, 50))

            self.draw_alien_info()

            self.play_button.draw_button()
            self.high_scores_button.draw_button()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if self.play_button.rect.collidepoint(mouse_pos):
                        return
                    elif self.high_scores_button.rect.collidepoint(mouse_pos):
                        self.show_high_scores()

            pg.display.flip()

    def show_high_scores(self):
        while True:
            self.screen.fill(self.bg_color)

            self.draw_high_scores()

            back_button = Button(self, "Back", center=(300, 100))
            back_button.draw_button()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if back_button.rect.collidepoint(mouse_pos):
                        return

            pg.display.flip()