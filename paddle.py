import pygame


class PlayerPaddle():
    def __init__(self, screen_width, screen_height):
        self.MOVEMENT_SPEED = 500
        self.PADDLE_WIDTH = 200
        self.PADDLE_HEIGHT = 50
        self.paddle = pygame.Rect(left=(screen_width / 2) - (self.PADDLE_WIDTH / 2),
                                  top=screen_height - 100, width=self.PADDLE_WIDTH, height=self.PADDLE_HEIGHT)
