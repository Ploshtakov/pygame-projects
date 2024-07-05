import pygame


# Functions
def display_board():
    """
    Resets the screen, drawing all symbols where needed
    :return: None
    """
    screen.fill(bg_color)

    # Display playing board
    x1, y1, x2, y2 = POS, POS, SIZE, SIZE
    for i in range(1, 10):
        pygame.draw.rect(screen, shadow, pygame.Rect(x1 + 1, y1 + 1, x2 + 1, y2 + 1), 3, 20)
        pygame.draw.rect(screen, yellow, pygame.Rect(x1, y1, x2, y2), 200, 20)

        x1 += SIZE + SPACE
        if i % 3 == 0:
            y1 += SPACE + SIZE
            x1 = POS

    # Display tittles
    display_tittles()

    # Display symbols
    for key, cords in board_cords.items():
        for cord in cords:
            display_symbol(cord[0], cord[1], key)

    # Display scores and names
    name_x, name_y = 10, 200
    size_between_score = 30
    size_between_names = 150

    text = font.render(player_1, True, shadow)
    screen.blit(text, (name_x + 1, name_y + 1))
    text = font.render(player_1, True, yellow)
    screen.blit(text, (name_x, name_y))

    text = font.render(str(scores["X"]), True, shadow)
    screen.blit(text, (name_x + 1, name_y + size_between_score + 1))
    text = font.render(str(scores["X"]), True, yellow)
    screen.blit(text, (name_x, name_y + size_between_score))

    text = font.render(player_2, True, shadow)
    screen.blit(text, (name_x + 1, name_y + size_between_names + 1))
    text = font.render(player_2, True, yellow)
    screen.blit(text, (name_x, name_y + size_between_names))

    text = font.render(str(scores["O"]), True, shadow)
    screen.blit(text, (name_x + 1, name_y + size_between_names + size_between_score + 1))
    text = font.render(str(scores["O"]), True, yellow)
    screen.blit(text, (name_x, name_y + size_between_names + size_between_score))

    text = font.render("ties", True, shadow)
    screen.blit(text, (name_x + 1, name_y + size_between_names * 2 + 1))
    text = font.render("ties", True, yellow)
    screen.blit(text, (name_x, name_y + size_between_names * 2))

    text = font.render(str(scores["None"]), True, shadow)
    screen.blit(text, (name_x + 1, name_y + size_between_names * 2 + size_between_score + 1))
    text = font.render(str(scores["None"]), True, yellow)
    screen.blit(text, (name_x, name_y + size_between_names * 2 + size_between_score))


def display_names_menu():
    """
    Draws names menu
    :return: None
    """
    screen.fill(bg_color)

    display_tittles()

    # Main window
    pygame.draw.rect(screen, shadow, pygame.Rect(250, 250, 303, 253), 3, 20)
    pygame.draw.rect(screen, pink, pygame.Rect(250, 250, 300, 250), 200, 20)
    pygame.draw.rect(screen, dark_pink, pygame.Rect(249, 249, 302, 252), 2, 20)

    # Main label
    text_type = font.render('Type your names:', True, purple)
    screen.blit(text_type, (280, 260))

    # Play button
    pygame.draw.rect(screen, shadow, pygame.Rect(340, 440, 130, 40), 20, 7)
    text_play = font.render('Play!', True, pink)
    screen.blit(text_play, (370, 445))

    update_names_menu()


def update_names_menu():
    """
    Updates input fields
    :return: None
    """
    if state == "names_1":
        pygame.draw.rect(screen, yellow, pygame.Rect(300, 320, 200, 40), 2, 7)
        pygame.draw.rect(screen, dark_pink, pygame.Rect(300, 370, 200, 40), 2, 7)
    elif state == "names_2":
        pygame.draw.rect(screen, dark_pink, pygame.Rect(300, 320, 200, 40), 2, 7)
        pygame.draw.rect(screen, yellow, pygame.Rect(300, 370, 200, 40), 2, 7)
    else:
        pygame.draw.rect(screen, dark_pink, pygame.Rect(300, 320, 200, 40), 2, 7)
        pygame.draw.rect(screen, dark_pink, pygame.Rect(300, 370, 200, 40), 2, 7)

    text_player_1 = font.render(player_1, True, purple)
    screen.blit(text_player_1, (310, 325))
    text_player_2 = font.render(player_2, True, purple)
    screen.blit(text_player_2, (310, 375))


def display_tittles():
    """
    Draws Tittle and "Made by KPL"
    :return: None
    """
    text_title = font_big.render('Tic-Tac-Toe', True, shadow)
    screen.blit(text_title, (138, 33))
    text_title = font_big.render('Tic-Tac-Toe', True, yellow)
    screen.blit(text_title, (135, 30))

    text_made = font_mid.render('Made by KPL', True, shadow)
    screen.blit(text_made, (521, 751))
    text_made = font_mid.render('Made by KPL', True, yellow)
    screen.blit(text_made, (520, 750))


def display_symbol(x, y, char):
    """
    Draws char at cords
    :param x: Middle point x
    :param y: Middle point y
    :param char: Char to draw
    :return: None
    """
    text_symbol = font_game.render(char, True, "#4b2e83")
    size = font_game.size(char)
    cords = (x - size[0] / 2, y - size[1] / 2 + 10)
    screen.blit(text_symbol, cords)


def animation_symbol(x, y, char):
    """
    Changes cursor to the char to play
    :param x: X cord of mouse
    :param y: Y cord of mouse
    :param char: Char to play
    :return:
    """
    display_board()  # Clears board_cords to remove previous char
    pygame.mouse.set_visible(False)  # Hides cursor
    text_symbol = font_mid.render(char, True, "#b4a0dd")
    try:
        size = font_mid.size(char)  # Gets size of char, so it can be centered
        screen.blit(text_symbol, (x - size[0] / 2, y - size[1] / 2 + 10))
    except TypeError:
        print(char)


def get_space_clicked(mouse_x, mouse_y, char):
    """
    Gets which space is clicked on board_cords, and adds it to board_cords dict
    :param mouse_x:
    :param mouse_y:
    :param char: Char to play
    :return: if clicked on valid space - next char to play, else return char
    """
    x1, y1, x2, y2 = POS, POS, SIZE, SIZE
    for i in range(1, 10):
        # Checks which vox is clicked, checks if its occupied
        if x1 <= mouse_x <= x1 + x2 and y1 <= mouse_y <= y1 + y2 and i not in board_spaces["X"] and i not in \
                board_spaces["O"]:
            x = x2 / 2 + x1
            y = y2 / 2 + y1
            board_cords[char].append((x, y))
            board_spaces[char].append(i)
            if char == "X":
                return "O"
            else:
                return "X"

        x1 += SIZE + SPACE
        if i % 3 == 0:
            y1 += SPACE + SIZE
            x1 = POS
    return char


def check_winner():
    """
    Checks if someone won
    :return: who won
    """
    x, o = 0, 0
    for combination in winning_combinations:
        for pos in combination:
            if pos in board_spaces["X"]:
                x += 1
            elif pos in board_spaces["O"]:
                o += 1
        if x == 3:
            return "X"
        elif o == 3:
            return "O"
        x, o = 0, 0

# Colors
bg_color = "#dbdcff"
shadow = "#7f7f7f"
pink = "#ffd4e5"
dark_pink = "#cca9b7"
purple = "#a68eb2"
light_blue = "#b2ffff"
yellow = "#feffa3"

# Vars
SIZE, POS, SPACE = 150, 160, 10
WIDTH, HEIGHT = 800, 800

player_1 = ""
player_2 = ""
scores = {"X": 0, "O": 0, "None": 0}

board_cords = {"X": [], "O": []}
board_spaces = {"X": [], "O": []}
to_play = "X"
state = "names_menu"

winning_combinations = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

# Init
pygame.init()
pygame.display.set_caption('Simple Tic-Tac-Toe -K')
screen_size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(screen_size)
screen.fill(bg_color)
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font('freesansbold.ttf', 28)
font_mid = pygame.font.Font('freesansbold.ttf', 40)
font_big = pygame.font.Font('freesansbold.ttf', 100)
font_game = pygame.font.Font('freesansbold.ttf', 160)

# Game loop
display_names_menu()  # Game always asks names first
running = True
while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()  # Mouse cords

    # Check if winner, or if board is full
    winner = check_winner()
    if winner:
        board_cords = {"X": [], "O": []}
        board_spaces = {"X": [], "O": []}
        to_play = winner
        scores[winner] += 1
    elif len(board_spaces["X"]) + len(board_spaces["O"]) == 9:
        board_cords = {"X": [], "O": []}
        board_spaces = {"X": [], "O": []}
        scores["None"] += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X button
            running = False

        # Mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and state in ["names_menu", "names_1", "names_2"]:  # While in names menu
                if 340 <= mouse[0] <= 340 + 130 and 440 <= mouse[1] <= 440 + 40:  # Play Button
                    state = "playing"
                    if player_1 == "":
                        player_1 = "Player X"
                    if player_2 == "":
                        player_2 = "Player O"
                elif 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 350:  # Name 1 field
                    state = "names_1"
                elif 300 <= mouse[0] <= 500 and 370 <= mouse[1] <= 400:  # Name 2 field
                    state = "names_2"
                else:
                    state = "names_menu"

            elif event.button == 1 and state == "playing":  # While playing, get which space is clicked
                to_play = get_space_clicked(mouse[0], mouse[1], to_play)

        # Key presses
        elif event.type == pygame.KEYDOWN:
            # Input for names
            key_name = pygame.key.name(event.key)
            if state == "names_1":
                if key_name == "backspace":  # Delete option
                    player_1 = player_1[:-1]
                elif len(player_1) < 8:  # Max length of 10
                    if len(key_name) == 1: # Allow only single chars (clicking shift produces "left shift")
                        player_1 += key_name

            elif state == "names_2":
                if key_name == "backspace":
                    player_2 = player_2[:-1]
                elif len(player_2) < 8:
                    if len(key_name) == 1:
                        player_2 += key_name

            display_names_menu()  # Update after each key pressed

        # Hover
        if state in ["names_menu", "names_1", "names_2"]:  # Hover effect for play button
            if 340 <= mouse[0] <= 340 + 130 and 440 <= mouse[1] <= 440 + 40:  # Play Button location
                pygame.draw.rect(screen, yellow, pygame.Rect(340, 440, 130, 40), 2, 7)
            else:
                pygame.draw.rect(screen, shadow, pygame.Rect(340, 440, 130, 40), 2, 7)

    # Update screen with correct layout
    if state == "playing":
        display_board()
    elif state in ["names_menu", "names_1", "names_2"]:
        update_names_menu()

    # Cursor change while playing, set to cursor to char to play
    if state == "playing":
        animation_symbol(mouse[0], mouse[1], to_play)

    pygame.display.flip()
pygame.quit()