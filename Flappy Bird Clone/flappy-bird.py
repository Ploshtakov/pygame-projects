import pygame
from random import randint
from time import sleep


# Functions
def draw_bird(x, y, angle):
    bird_image = pygame.transform.rotate(bird, angle)
    screen.blit(bird_image, (x - SIZE_BIRD[0] / 2, y - SIZE_BIRD[1] / 2))


def draw_pipes(x, y, size_hole):
    screen.blit(pipe_up, (x, y - SIZE_PIPE[1] - size_hole))
    screen.blit(pipe_down, (x, y + size_hole))


def draw_clouds(x, y, type, angle):
    cloud_image = ""
    if type == 1:
        cloud_image = cloud1
    elif type == 2:
        cloud_image = cloud2
    elif type == 3:
        cloud_image = cloud3
    elif type == 4:
        cloud_image = cloud4

    cloud_image = pygame.transform.rotate(cloud_image, angle)
    screen.blit(cloud_image, (x, y))


def draw_score(points):
    text_player_1 = font.render(f"Score: {points}", True, shadow)
    screen.blit(text_player_1, (12, 12))
    text_player_1 = font.render(f"Score: {points}", True, score_color)
    screen.blit(text_player_1, (10, 10))


def generate_pipe(last_y, last_hole, last_dist):
    x = WIDTH
    if last_y < 70:
        y = last_y + randint(20, 50)
    elif last_y > 730:
        y = last_y + randint(-50, -20)
    else:
        y = last_y + randint(-50, 50)
    if last_hole < 80:
        hole = last_hole + randint(3, 15)
    else:
        hole = last_hole + randint(-20, 15)

    if last_dist < 200:
        dist = last_dist + randint(5, 20)
    else:
        dist = last_dist + randint(-20, 20)
    dist = last_dist - 1
    return (x, y, hole, dist)


def generate_cloud():
    x = WIDTH
    y = randint(0, 150)
    type = randint(1, 4)
    angle = randint(0, 1) * 180
    dist = randint(200, 500)
    return (x, y, type, angle, dist)


def pipe_collision(pipe, space, bird):
    valid_hole = (pipe - space, pipe + space)
    return not (valid_hole[0] < bird < valid_hole[1])


def dead_screen():
    text_player_1 = font.render(f"You died!", True, shadow)
    screen.blit(text_player_1, (402, 402))
    text_player_1 = font.render(f"You died!", True, "red")
    screen.blit(text_player_1, (400, 400))
    pygame.display.flip()
    sleep(1)


# Colors
bg_color = "#76c9d4"
shadow = "#7f7f7f"
score_color = "#f0c85d"

# Vars
WIDTH, HEIGHT = 1000, 800
SIZE_BIRD = [85, 60]
SIZE_PIPE = [120, 960]
bird_x = 200
bird_y = 200
bird_angle = -1
JUMP = 150
to_jump = 0
gravity = 1
pipes_to_remove = False
clouds_to_remove = False
pipe_speed = 10
pipe_size_hole = 120
pipe_distance_between = 400
pipes_on_screen = [(WIDTH, 400, pipe_size_hole,
                    pipe_distance_between)]  # Start x, Center of hole (y), Size of hole, distance between next pipe
clouds_on_screen = [(WIDTH, 100, 1, 0, 300)]  # x, y, type, angle, distance

score = 0

# Init
pygame.init()
pygame.display.set_caption('Flappy bird clone -K')
screen_size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

# Images
icon = pygame.image.load("images/bird_icon.png").convert_alpha()
bird = pygame.image.load("images/bird.png").convert_alpha()
pipe_up = pygame.image.load("images/pipe_up.png").convert_alpha()
pipe_down = pygame.image.load("images/pipe_down.png").convert_alpha()
cloud1 = pygame.image.load("images/cloud1.png").convert_alpha()
cloud2 = pygame.image.load("images/cloud2.png").convert_alpha()
cloud3 = pygame.image.load("images/cloud3.png").convert_alpha()
cloud4 = pygame.image.load("images/cloud4.png").convert_alpha()

pygame.display.set_icon(icon)

# Game loop
running = True
while running:
    screen.fill(bg_color)

    clock.tick(30)
    mouse = pygame.mouse.get_pos()

    # Score & collision
    if (pipes_on_screen[0][0] == bird_x or pipes_on_screen[0][0] + SIZE_PIPE[0] / 2 == bird_x
            or pipes_on_screen[0][0] + SIZE_PIPE[0] == bird_x):  # 3 checks for collision for each pipe
        if pipe_collision(pipes_on_screen[0][1], pipes_on_screen[0][2], bird_y):
            running = False
            dead_screen()
        elif pipes_on_screen[0][0] + SIZE_PIPE[0] == bird_x:
            score += 1


        
    # Draw
    for cloud_cords in clouds_on_screen:
        draw_clouds(cloud_cords[0], cloud_cords[1], cloud_cords[2], cloud_cords[3])
    draw_bird(bird_x, bird_y, bird_angle)
    for pipe_cords in pipes_on_screen:
        draw_pipes(pipe_cords[0], pipe_cords[1], pipe_cords[2])
    draw_score(score)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            to_jump = JUMP
            bird_angle = 40
            gravity = 5

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                to_jump = JUMP
                bird_angle = 40
                gravity = 5

    # Bird
    if to_jump > 10:
        to_jump -= to_jump / 8
        bird_y -= to_jump / 8
        bird_angle -= to_jump / 20
    else:
        gravity *= 1.04
        bird_angle *= 1.05
    bird_y += gravity
    
    if bird_y > HEIGHT:
        bird_y = HEIGHT
    elif bird_y < 0:
        bird_y = 0 

    # Pipes
    for i in range(len(pipes_on_screen)):  # Move pipes
        pipe_x, pipe_y, pipe_hole, pipe_distance = pipes_on_screen[i]
        if pipe_x - pipe_speed < -SIZE_PIPE[0]:
            pipes_to_remove = True
        else:
            pipes_on_screen[i] = (pipe_x - pipe_speed, pipe_y, pipe_hole, pipe_distance)

    if pipes_to_remove:
        del pipes_on_screen[0]
        pipes_to_remove = False

    if pipes_on_screen[-1][0] < WIDTH - pipes_on_screen[-1][3]:
        pipe_x, pipe_y, pipe_hole, pipe_distance = pipes_on_screen[-1]
        pipes_on_screen.append(generate_pipe(pipe_y, pipe_hole, pipe_distance))

    # Clouds
    for i in range(len(clouds_on_screen)):  # Move clouds
        cloud_x, cloud_y, cloud_type, cloud_angle, cloud_distance = clouds_on_screen[i]
        if cloud_x - pipe_speed < -100:
            clouds_to_remove = True
        else:
            clouds_on_screen[i] = (cloud_x - (pipe_speed + 3), cloud_y, cloud_type, cloud_angle, cloud_distance)

    if clouds_to_remove:
        del clouds_on_screen[0]
        clouds_to_remove = False

    if clouds_on_screen[-1][0] < WIDTH - clouds_on_screen[-1][4]:
        cloud_x, cloud_y, cloud_type, cloud_angle, cloud_distance = clouds_on_screen[-1]
        clouds_on_screen.append(generate_cloud())

    pygame.display.flip()
pygame.quit()
