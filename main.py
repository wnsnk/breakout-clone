import pygame
from paddle import PlayerPaddle
import random

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PADDLE_WIDTH = 300
PADDLE_HEIGHT = 30
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
delta_time = clock.tick(60) / 1000
MOVEMENT_SPEED = 500
ball_speed = 400
ball_degrees = random.randint(-75, 75)
ball_degrees = 75
player_paddle = pygame.Rect((SCREEN_WIDTH / 2) - (PADDLE_WIDTH / 2),
                            SCREEN_HEIGHT - 100, PADDLE_WIDTH, PADDLE_HEIGHT)

ball_movement_x = ball_degrees * delta_time
ball_movement_y = ball_speed * delta_time
ball_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def check_paddle_wall_collision():
    if player_paddle.left < 0:
        print('hit wall left!!')
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)
    elif (player_paddle.right) > SCREEN_WIDTH:
        print('hit wall right!!')
        player_paddle.move_ip(-MOVEMENT_SPEED * delta_time, 0)


def check_ball_paddle_collision():
    global ball_movement_y
    if player_paddle.top <= ball_position.y and player_paddle.left < ball_position.x < player_paddle.right:
        ball_movement_y *= -1


def check_ball_wall_collision():
    global ball_movement_y, ball_movement_x
    if ball_position.x < 0 or ball_position.x > SCREEN_WIDTH:
        ball_movement_x *= -1
    if ball_position.y < 0:
        ball_movement_y *= -1


def check_ball_block_collision(block: Block):
    global ball_movement_y, ball_movement_x
    # bottom and top
    if block.rectangle.left < ball_position.x < block.rectangle.right:
        if block.rectangle.top < ball_position.y < block.rectangle.bottom:
            block.hit_points -= 1
            ball_movement_y *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True

        if block.rectangle.top > ball_position.y > block.rectangle.bottom:
            block.hit_points -= 1
            ball_movement_x *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True
            print('hit top')
    # left and right
    if block.rectangle.top > ball_position.y > block.rectangle.top:
        if ball_position.x > block.rectangle.left or ball_position.x < block.rectangle.right:
            block.hit_points -= 1
            ball_movement_y *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True
            print('hit side')


def get_positions():
    print('x ball:', ball_position.x)
    print('y ball: ', ball_position.y)
    print('paddle left', player_paddle.left)
    print('player paddle_right', player_paddle.right)
    print('top player paddle: ', player_paddle.top)


class Block():
    def __init__(self, Rect: pygame.Rect, hit_points):
        self.rectangle = Rect
        self.remove = False
        self.hit_points = hit_points
        if self.hit_points <= 0:
            self.remove = True
        else:
            self.color = self.change_color()

    def change_color(self):
        if self.hit_points == 1:
            self.color = 'purple'
        elif self.hit_points <= 2:
            self.color = 'blue'
        elif self.hit_points <= 5:
            self.color = 'green'
        elif self.hit_points <= 10:
            self.color = 'yellow'
        elif self.hit_points <= 15:
            self.color = 'orange'
        else:
            self.color = 'red'
        return self.color


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
    pygame.draw.circle(screen, 'white', ball_position, 10)
    ball_position.x += ball_movement_x
    ball_position.y += ball_movement_y
    for block in blocks:
        count += 1
        try:
            pygame.draw.rect(
                screen, block.color, block.rectangle)
        except IndexError:
            color_num = 0
        if count % 10 == 0:
            color_num += 1

        check_ball_block_collision(block=block)
        if block.remove:
            blocks.remove(block)
            ball_movement_y *= 1.03
            player_paddle.width -= 5
            ball_movement_x += random.randint(-10, 10)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_paddle.move_ip(-(MOVEMENT_SPEED * delta_time), 0)
    if keys[pygame.K_d]:
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)
    if keys[pygame.K_p]:
        get_positions()

    # flip() the display to put your work on screen

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    delta_time = clock.tick(60) / 1000
    check_paddle_wall_collision()
    check_ball_wall_collision()
    check_ball_paddle_collision()
    pygame.display.update()
    print(ball_speed)

pygame.quit()
