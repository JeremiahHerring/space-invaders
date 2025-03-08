import pygame as pg
import sys
from button import Button

class DeathScreen:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.screen_rect = self.screen.get_rect()
        self.bg_color = self.settings.bg_color

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)

        self.play_again_button = Button(self, "Play Again", center=(self.screen_rect.centerx, self.screen_rect.centery + 50))
        self.quit_button = Button(self, "Quit", center=(self.screen_rect.centerx, self.screen_rect.centery + 120))

    def draw_text(self, text, y_offset):
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery + y_offset))
        self.screen.blit(text_surface, text_rect)

    def run(self):
        """Display the death screen and handle input."""
        while True:
            self.screen.fill(self.bg_color)
            
            self.draw_text("Game Over", -100)
            self.draw_text(f"Final Score: {self.stats.score:,}", -50)
            
            self.play_again_button.draw_button()
            self.quit_button.draw_button()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    if self.play_again_button.rect.collidepoint(mouse_pos):
                        print("play again printed here")
                        return "play_again"
                    elif self.quit_button.rect.collidepoint(mouse_pos):
                        return "quit"
            
            pg.display.flip()
