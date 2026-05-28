import pygame
from paddle import PlayerPaddle

# pygame setup
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
delta_time = 0
MOVEMENT_SPEED = 500

player_paddle = pygame.Rect((SCREEN_WIDTH / 2) - (PADDLE_WIDTH / 2),
                            SCREEN_HEIGHT - 100, PADDLE_WIDTH, PADDLE_HEIGHT)


class Block():
    def __init__(self, top: float, left: float):
        self.width = 200
        self.height = 25
        self.rectangle = pygame.Rect(
            top=top, left=left, width=self.width, height=self.height)


block_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
BLOCK_WIDTH = ((SCREEN_WIDTH - 10) / 10) - 5
BLOCK_HEIGHT = 20
block_x = 10
block_y = 20
blocks = []
for _ in range(len(block_colors)):
    for _ in range(10):
        block = pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append(block)
        block_x += BLOCK_WIDTH + BLOCK_HEIGHT
    block_x = 10
    block_y += BLOCK_HEIGHT + 10
    print('hi')

count = 0
color_num = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill('black')

    pygame.draw.rect(screen, 'white', player_paddle)
    for block in blocks:
        count += 1
        if count < len(blocks):
            try:
                pygame.draw.rect(screen, block_colors[color_num], block)
            except IndexError:
                color_num = 0
        if count % 10 == 0:
            color_num += 1
        # if count > len(blocks):

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_paddle.move_ip(-(MOVEMENT_SPEED * delta_time), 0)
    if keys[pygame.K_d]:
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)

    # flip() the display to put your work on screen

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    delta_time = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()
