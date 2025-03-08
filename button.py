import pygame as pg

class Button:
    def __init__(self, ai_game, msg, center=None):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # Green
        self.text_color = (255, 255, 255)  # White
        self.font = pg.font.SysFont(None, 48)

        self.rect = pg.Rect(0, 0, self.width, self.height)
        if center:
            self.rect.center = center
        else:
            self.rect.center = self.screen_rect.center

        self.msg = msg
        self._prep_msg(self.msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def reset_message(self, new_msg):
        """Update the button text dynamically."""
        self._prep_msg(new_msg)
