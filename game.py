import pygame
import random
import urllib

pygame.init()


pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
DARK_CYAN = (123, 104, 238)
YELLOW = (247, 255, 0)

game_title = 'Retro Worm'
display_width = 800
display_height = 600
background_color = BLACK
snake_color = DARK_CYAN
energy_color = DARK_CYAN
polygon_powerup_color = (random.randrange(255), random.randrange(255), random.randrange(255))

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption(game_title)

global block_size
block_size = 10

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)

def get_collision(p_x, p_y, target_x, target_y, width, height):
    if p_x >= target_x and p_x <= target_x + width:
        if p_y >= target_y and p_y <= target_y + height:
            return True
    return False


def snake(width, height, snakelist):
    for x_and_y in snakelist:
        pygame.draw.rect(game_display, snake_color, [x_and_y[0], x_and_y[1], width, height])
        pygame.draw.rect(game_display, WHITE, [x_and_y[0] + 2, x_and_y[1] + 2, width, height])


def create_bombs(amount):
    bomb_x = list()
    bomb_y = list()
    for am in range(amount):
        bomb_x.append(random.randrange((display_width - block_size) - 30))
        bomb_y.append(30)

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    game_display.blit(screen_text, [200, 300])


def display_score(score):
    screen_text = font.render(score, True, YELLOW)
    game_display.blit(screen_text, [50, 50])


def game_loop():
    pygame.mixer.music.rewind()
    pygame.mixer.music.play(1000)
    fps = 30

    running = True
    game_over = False

    global block_size
    block_size = 10

    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = 0
    lead_y_change = 0

    powerup_x = 0
    powerup_y = 0

    snake_list = list()
    snake_length = 1

    rand_apple_x = round(random.randrange(0, display_width - block_size) / float(block_size)) * block_size
    rand_apple_y = round(random.randrange(0, display_height - block_size) / float(block_size)) * block_size

    score = 0
    score_add = 10

    up_bombs_x = [random.randrange(0, display_width - block_size),
                  random.randrange(0, display_width - block_size),
                  random.randrange(0, display_width - block_size),
                  random.randrange(0, display_width - block_size)]

    up_bombs_y = [0,
                  0,
                  0,
                  0]

    left_bombs_x = [0,
                    0,
                    0,
                    0]

    left_bombs_y = [random.randrange(0, display_height - block_size),
                    random.randrange(0, display_height - block_size),
                    random.randrange(0, display_height - block_size),
                    random.randrange(0, display_height - block_size)]

    background_color = (random.randrange(255), random.randrange(255), random.randrange(255))

    while running:
        while game_over:
            game_display.fill(background_color)
            message_to_screen('Game over. Press R to restart or Q to quit.', DARK_CYAN)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False
                    if event.key == pygame.K_r:
                        game_loop()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Key handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                if event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_f:
                    block_size += 10
                elif event.key == pygame.K_e:
                    block_size -= 10
        # Map limits
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        up_bombs_y[0] += block_size
        up_bombs_y[1] += block_size
        up_bombs_y[2] += block_size
        up_bombs_y[3] += block_size

        left_bombs_x[0] += block_size
        left_bombs_x[1] += block_size
        left_bombs_x[2] += block_size
        left_bombs_x[3] += block_size

        powerup_x += 5
        powerup_y += 5

        # Clean state
        game_display.fill(background_color)
        # Draw
        pygame.draw.rect(game_display, energy_color, [rand_apple_x, rand_apple_y, block_size, block_size])
        pygame.draw.rect(game_display, YELLOW, [up_bombs_x[0], up_bombs_y[0], block_size, block_size])
        pygame.draw.rect(game_display, YELLOW, [up_bombs_x[1], up_bombs_y[1], block_size, block_size])
        pygame.draw.rect(game_display, YELLOW, [up_bombs_x[2], up_bombs_y[2], block_size, block_size])
        pygame.draw.rect(game_display, YELLOW, [up_bombs_x[3], up_bombs_y[3], block_size, block_size])

        if score >= 100:
            pygame.draw.rect(game_display, YELLOW, [left_bombs_x[0], left_bombs_y[0], block_size, block_size])
            pygame.draw.rect(game_display, YELLOW, [left_bombs_x[1], left_bombs_y[1], block_size, block_size])
            pygame.draw.rect(game_display, YELLOW, [left_bombs_x[2], left_bombs_y[2], block_size, block_size])
            pygame.draw.rect(game_display, YELLOW, [left_bombs_x[3], left_bombs_y[3], block_size, block_size])
            block_size = 20

        pygame.draw.circle(game_display, DARK_CYAN, [powerup_x, powerup_x], 10)

        snake_head = list()
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # for each_segment in snake_list[:-1]:
        #   if each_segment == snake_head:
        #      game_over = True

        snake(block_size, block_size, snake_list)
        display_score('Score: ' + str(score))
        pygame.display.update()

        for index in range(len(up_bombs_x) - 1):
            if get_collision(lead_x, lead_y, up_bombs_x[index], up_bombs_y[index], 10, 10):
                game_over = True
        if score >= 100:
            for index in range(len(left_bombs_x) - 1):
                if get_collision(lead_x, lead_y, left_bombs_x[index], left_bombs_y[index], 10, 10):
                    game_over = True

        # APPLE COLLISION
        if lead_x >= rand_apple_x and lead_x <= rand_apple_x + block_size:
            if lead_y >= rand_apple_y and lead_y <= rand_apple_y + block_size:
                rand_apple_x = round(random.randrange(0, display_width - block_size) / block_size) * block_size
                rand_apple_y = round(random.randrange(0, display_height - block_size) / block_size) * block_size
                snake_length += 1
                score += score_add
                display_score(str(score))
                background_color = (random.randrange(255), random.randrange(255), random.randrange(255))

        if get_collision(lead_x, lead_y, powerup_x, powerup_y, block_size, block_size):
            score += 50
            powerup_x = 1000
            powerup_y = 1000

        if up_bombs_y[0] >= display_height or up_bombs_y[0] <= 0:
            up_bombs_x = [random.randrange(0, display_width - block_size),
                          random.randrange(0, display_width - block_size),
                          random.randrange(0, display_width - block_size),
                          random.randrange(0, display_width - block_size),
                          random.randrange(0, display_width - block_size)]
            up_bombs_y = [0, 0, 0, 0]

        if left_bombs_x[0] >= display_width or left_bombs_y[0] <= 0:
            left_bombs_y = [random.randrange(0, display_width - block_size),
                            random.randrange(0, display_width - block_size),
                            random.randrange(0, display_width - block_size),
                            random.randrange(0, display_width - block_size),
                            random.randrange(0, display_width - block_size)]
            left_bombs_x = [0, 0, 0, 0]

        random_spawn_powerup = random.randrange(1000)
        if random_spawn_powerup == 999:
            powerup_x = 0
            powerup_y = 0
        clock.tick(fps)

    pygame.quit()
    quit()

# CODE
game_loop()
