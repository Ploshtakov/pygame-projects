# First game in pygame
# This was fun :)
# Made by KalinPl

import pygame
from time import sleep
from random import randint, choice
from math import ceil

pygame.init()
pygame.display.set_caption('Simple Snake -K')
screen_size = [650, 650]
screen = pygame.display.set_mode(screen_size)

font = pygame.font.Font('freesansbold.ttf', 20)

bg_color = [20, 20, 50]
yellow = [255, 255, 0]
red = [255, 0, 0]
green = [34, 139, 34]

score = 0
direction = choice(["W", "A", "S", "D"])


def get_pixel_cords(cord_x, cord_y, size):
    pixel_x = cord_x * 50 - (size / 2)
    pixel_y = cord_y * 50 - (size / 2)

    stats = [pixel_x, pixel_y, size, size]
    return stats


def render_tail():
    size_tail = 44
    x, y, z = 235, 235, 0

    for element in head_cords_history:
        pygame.draw.rect(screen, (x, y, z), pygame.Rect(get_pixel_cords(element[0], element[1], size_tail)))
        size_tail -= 1
        x -= 2
        y -= 3

        if size_tail < 4:
            size_tail = 4
        if y < 85:
            x, y = 105, 85


def render_score(scr):
    text = font.render(f'Score: {scr}', True, yellow)
    text_rect = text.get_rect()
    text_rect.center = (70, 15)
    screen.blit(text, text_rect)


def move_head(direct):
    if direct == "W":
        head_cords[1] -= 1
    elif direct == "S":
        head_cords[1] += 1
    elif direct == "A":
        head_cords[0] -= 1
    elif direct == "D":
        head_cords[0] += 1


def get_empty_spot(history):
    cords = [randint(1, 12), randint(1, 12)]

    while cords in history:
        cords = [randint(1, 12), randint(1, 12)]
    else:
        return cords


def check_if_dead(head, history):
    return (head in history[1:]) or (head[0] < 1) or (head[0] > 12) or (head[1] < 1) or (head[1] > 12)


def dead(s):
    pygame.draw.rect(screen, red, pygame.Rect(0, 0, 650, 650), 25)

    text = font.render(f'You died! Score: {s}', True, yellow)
    text_rect = text.get_rect()
    text_rect.center = (325, 325)
    screen.blit(text, text_rect)

    pygame.display.flip()


head_cords = [randint(5, 7), randint(5, 7)]
head_cords_history = [head_cords[:]]
length_snake = 3

berry_cords = get_empty_spot(head_cords_history)
spec_berry_cords = [-1, -1]

running = True
running_end = False
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_w and direction in ["A", "D"]:
                direction = "W"
                break
            elif event.key == pygame.K_s and direction in ["A", "D"]:
                direction = "S"
                break
            elif event.key == pygame.K_a and direction in ["W", "S"]:
                direction = "A"
                break
            elif event.key == pygame.K_d and direction in ["W", "S"]:
                direction = "D"
                break


    # Border
    screen.fill((100, 0, 100))

    # Field
    pygame.draw.rect(screen, bg_color, pygame.Rect(25, 25, 600, 600))

    # Spec berry
    pygame.draw.rect(screen, green, pygame.Rect(get_pixel_cords(spec_berry_cords[0], spec_berry_cords[1], 15)))

    # Berry
    pygame.draw.rect(screen, red, pygame.Rect(get_pixel_cords(berry_cords[0], berry_cords[1], 20)))

    # Head
    render_tail()
    move_head(direction)
    pygame.draw.rect(screen, yellow, pygame.Rect(get_pixel_cords(head_cords[0], head_cords[1], 45)))

    if check_if_dead(head_cords, head_cords_history):
        dead(score)
        running_end = True
        break

    head_cords_history.insert(0, head_cords[:])
    head_cords_history = head_cords_history[:length_snake]

    # Check for berries
    if head_cords == berry_cords:
        score += 1
        length_snake += 1
        berry_cords = get_empty_spot(head_cords_history)

        if randint(1, 10) == 1:
            spec_berry_cords = get_empty_spot(head_cords_history)
        else:
            spec_berry_cords = [-1, -1]

    elif head_cords == spec_berry_cords:
        score += 10
        length_snake = ceil(length_snake / 1.5)
        spec_berry_cords = [-1, -1]

    # Score
    render_score(score)

    # Refresh screen
    pygame.display.flip()

    # 5FPS
    sleep(0.2)

while running_end:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_end = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running_end = False

pygame.quit()
