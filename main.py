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


def check_paddle_wall_collision():
    if player_paddle.left < 0:
        print('hit wall left!!')
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)
    elif (player_paddle.left + PADDLE_WIDTH) > SCREEN_WIDTH:
        print('hit wall right!!')
        player_paddle.move_ip(-MOVEMENT_SPEED * delta_time, 0)


class Block():
    def __init__(self, Rect: pygame.Rect, hit_points):
        self.rectangle = Rect
        self.remove = False
        self.hit_points = hit_points
        if hit_points <= 0:
            self.remove = True
        elif self.hit_points <= 1:
            self.color = 'purple'
        elif self.hit_points <= 2:
            self.color = 'blue'
        elif self.hit_points <= 5:
            self.color = 'green'
        elif hit_points <= 10:
            self.color = 'yellow'
        elif self.hit_points <= 15:
            self.color = 'orange'
        else:
            self.color = 'red'


hit_points = [20, 15, 10, 5, 2, 1]
BLOCK_WIDTH = ((SCREEN_WIDTH - 10) / 10) - 5
BLOCK_HEIGHT = 20
block_x = 10
block_y = 20
blocks = []
for hp in hit_points:
    for _ in range(10):
        block = pygame.Rect(block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT)
        block = Block(block, hp)
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

        try:
            pygame.draw.rect(
                screen, block.color, block.rectangle)
        except IndexError:
            color_num = 0
        if count % 10 == 0:
            color_num += 1

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
    check_paddle_wall_collision()
    pygame.display.update()

pygame.quit()
