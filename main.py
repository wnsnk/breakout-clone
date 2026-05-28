import pygame
import random
import csv
from operator import itemgetter

USERNAME = 'wnsnk'

pygame.init()
pygame.font.init()

print(pygame.font.get_init())

GAME_FONT = pygame.font.Font(pygame.font.get_default_font(), size=50)

score = 0
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
paddle_width = 300
PADDLE_HEIGHT = 20
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_over_ = False
delta_time = clock.tick(60) / 1000
MOVEMENT_SPEED = 500
ball_speed = 400
ball_degrees = random.randint(-75, 75)
ball_degrees = 75
player_paddle = pygame.Rect((SCREEN_WIDTH / 2) - (paddle_width / 2),
                            SCREEN_HEIGHT - 100, paddle_width, PADDLE_HEIGHT)

ball_movement_x = ball_degrees * delta_time
ball_movement_y = ball_speed * delta_time
ball_position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def check_paddle_wall_collision():
    if player_paddle.left < 0:
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)
    elif (player_paddle.right) > SCREEN_WIDTH:
        player_paddle.move_ip(-MOVEMENT_SPEED * delta_time, 0)


def check_ball_paddle_collision():
    global ball_movement_y
    if player_paddle.top <= ball_position.y and player_paddle.left < ball_position.x < player_paddle.right:
        ball_movement_y *= -1


def check_ball_wall_collision():
    global ball_movement_y, ball_movement_x, game_over_
    if ball_position.x < 0 or ball_position.x > SCREEN_WIDTH:
        ball_movement_x *= -1
    if ball_position.y < 0:
        ball_movement_y *= -1
    if ball_position.y > (SCREEN_HEIGHT + 20) or ball_position.y < -20 or ball_position.x < -20 or ball_position.x > (SCREEN_WIDTH + 20):
        if not game_over_:
            game_over_ = True
            game_over()


def check_ball_block_collision(block: Block):
    global ball_movement_y, ball_movement_x, score
    # bottom and top
    if block.rectangle.left < ball_position.x < block.rectangle.right:
        if block.rectangle.top < ball_position.y < block.rectangle.bottom:
            block.hit_points -= 1
            score += 1
            ball_movement_y *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True

        if block.rectangle.top > ball_position.y > block.rectangle.bottom:
            block.hit_points -= 1
            score += 1
            ball_movement_x *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True

    # left and right
    if block.rectangle.top > ball_position.y > block.rectangle.top:
        if ball_position.x > block.rectangle.left or ball_position.x < block.rectangle.right:
            block.hit_points -= 1
            score += 1
            ball_movement_y *= -1
            if block.hit_points > 0:
                block.change_color()
            else:
                block.remove = True


def get_positions():
    print('x ball:', ball_position.x)
    print('y ball: ', ball_position.y)
    print('paddle left', player_paddle.left)
    print('player paddle_right', player_paddle.right)
    print('top player paddle: ', player_paddle.top)


def game_over():
    global running
    try:
        with open('HIGHSCORES.csv', 'r') as highscores_csv:
            highscores = csv.DictReader(highscores_csv)
            highscores = list(highscores)
            for hs in highscores:
                hs['high_score'] = int(hs['high_score'])
    except FileNotFoundError:
        with open('HIGHSCORES.csv', 'a') as highscores_csv:
            fields = ['name', 'high_score']
            new_row = {'name': USERNAME, 'high_score': score}
            writer = csv.DictWriter(highscores_csv, fieldnames=fields)
            writer.writeheader()
            writer.writerow(new_row)
    try:
        if score > highscores[0]['high_score']:
            with open('HIGHSCORES.csv', 'a') as highscores_csv:

                new_row = {'name': USERNAME, 'high_score': score}
                writer = csv.DictWriter(highscores_csv, fieldnames=fields)
                writer.writerow(new_row)
                highscores.append(new_row)
    except UnboundLocalError:
        new_row = {'name': 'None', 'high_score': 0}
        highscores = []
        highscores.append(new_row)
    highscores.sort(key=itemgetter('high_score'), reverse=True)

    game_over_text = f'GAME OVER\nName  Highscore   \n{highscores[0]['name']}   {highscores[0]['high_score']}\n\nYour score: {score}'
    render_game_over_text = GAME_FONT.render(game_over_text, True, 'white')
    screen.blit(render_game_over_text, ((SCREEN_WIDTH / 2) -
                text_width, (SCREEN_HEIGHT / 2) - text_height))


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
            ball_movement_y *= 1.02
            player_paddle.width -= 5
            ball_movement_x += random.randint(-5, 5)
            score += 5

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player_paddle.move_ip(-(MOVEMENT_SPEED * delta_time), 0)
    if keys[pygame.K_d]:
        player_paddle.move_ip(MOVEMENT_SPEED * delta_time, 0)
    if keys[pygame.K_p]:
        get_positions()

    delta_time = clock.tick(60) / 1000
    check_paddle_wall_collision()
    check_ball_wall_collision()
    check_ball_paddle_collision()

    scoreboard_text = f'Score: {score}'
    scoreboard = GAME_FONT.render(scoreboard_text, True, 'white')
    text_width, text_height = GAME_FONT.size(scoreboard_text)
    screen.blit(scoreboard, (0, (SCREEN_HEIGHT - text_height)))
    if game_over_:
        game_over()
    pygame.display.update()


pygame.quit()
