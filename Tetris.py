import pygame
import random
import time
from os import path
import sys

from pygame.constants import *

pygame.font.init()

# Constants
W_H = 600

WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 255, 0)
BLUE = (0, 191, 255)

file_path = path.abspath(__file__)  # full path of Tetris.py
dir_path = path.dirname(file_path)  # full path of the directory
bg_jpg = path.join(dir_path, 'bg.jpg')  # absolute background image path
retro_font = path.join(dir_path, 'retro.ttf')  # absolute font path

# Current theme
SELECTED_color = WHITE

# Blocks layout (4x4)
S = [[0, 1, 1, 0,
      1, 1, 0, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [1, 0, 0, 0,
      1, 1, 0, 0,
      0, 1, 0, 0,
      0, 0, 0, 0]]

Z = [[1, 1, 0, 0,
      0, 1, 1, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [0, 0, 1, 0,
      0, 1, 1, 0,
      0, 1, 0, 0,
      0, 0, 0, 0]]

T = [[0, 1, 0, 0,
      1, 1, 1, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [0, 0, 1, 0,
      0, 1, 1, 0,
      0, 0, 1, 0,
      0, 0, 0, 0],

     [1, 1, 1, 0,
      0, 1, 0, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [1, 0, 0, 0,
      1, 1, 0, 0,
      1, 0, 0, 0,
      0, 0, 0, 0]]

O = [[0, 1, 1, 0,
      0, 1, 1, 0,
      0, 0, 0, 0,
      0, 0, 0, 0]]

I = [[1, 1, 1, 1,
      0, 0, 0, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [1, 0, 0, 0,
      1, 0, 0, 0,
      1, 0, 0, 0,
      1, 0, 0, 0]]

J = [[1, 0, 0, 0,
      1, 1, 1, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [0, 1, 0, 0,
      0, 1, 0, 0,
      1, 1, 0, 0,
      0, 0, 0, 0],

     [1, 1, 1, 0,
      0, 0, 1, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [1, 1, 0, 0,
      1, 0, 0, 0,
      1, 0, 0, 0,
      0, 0, 0, 0]]

L = [[0, 0, 0, 1,
      0, 1, 1, 1,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [0, 0, 1, 1,
      0, 0, 0, 1,
      0, 0, 0, 1,
      0, 0, 0, 0],

     [0, 1, 1, 1,
      0, 1, 0, 0,
      0, 0, 0, 0,
      0, 0, 0, 0],

     [0, 0, 1, 0,
      0, 0, 1, 0,
      0, 0, 1, 1,
      0, 0, 0, 0]]

blockSize = 30  # Set the size of the grid block
total_blocks = 20
occupied = []  # Blocks on floor/stacked on top of each other


def draw_grid(WINDOW):
    """Draw initial grid"""

    for x in range(0, W_H, blockSize):
        for y in range(0, W_H, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(WINDOW, BLACK, rect, 1)

    pygame.draw.line(WINDOW, (139, 0, 0), (W_H, 0), (W_H, W_H), 1)

    for x in range((W_H + 30), (W_H + 200), blockSize):
        for y in range(230, W_H, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(WINDOW, BLACK, rect, 1)


def spawn_block(WINDOW, block):
    """Spawn a block on screen"""
    y = 0 * blockSize
    x = random.randint(0, 16) * blockSize
    _X = x
    _Y = y
    row = 4

    for value in block[0]:
        if value == 0:
            pass
        else:
            rect = pygame.Rect(x, y, blockSize, blockSize)
            WINDOW.fill(SELECTED_color, rect)
        row -= 1
        x += blockSize
        if row == 0:
            y += blockSize
            x = _X
            row = 4

    old = []
    plus = 0
    _plus = 0
    for p in block[0]:
        if p == 1:
            old.append([(_X + plus), (_Y + _plus)])
        else:
            old.append([str((_X + plus)), (_Y + _plus)])
        plus += blockSize
        if plus == (4 * blockSize):
            _plus += blockSize
            plus = 0

    draw_grid(WINDOW)
    return old, block


def move_y_axis(WINDOW, block):
    """Move y-axis coordinate regularly"""
    old = []

    for pix in block:
        if isinstance(pix[0], int):
            if [pix[0], (pix[1] + blockSize)] in occupied or (pix[1] + blockSize) >= W_H:

                for oc in block:
                    if isinstance(oc[0], int):
                        occupied.append(oc)

                return block, True

    for pix in block:
        if isinstance(pix[0], int):
            rect = pygame.Rect(pix[0], pix[1], blockSize, blockSize)
            WINDOW.fill(BLACK, rect)

    for pix in block:
        if isinstance(pix[0], int):
            rect = pygame.Rect(pix[0], (pix[1] + blockSize), blockSize, blockSize)
            old.append([pix[0], (pix[1] + blockSize)])
            WINDOW.fill(SELECTED_color, rect)

    draw_grid(WINDOW)
    return old, False


def move_x_axis(WINDOW, block, direction):  # Direction is -1 for left and +1 for right
    """User left right control"""

    old = []
    movement = direction * blockSize

    for pix in block:
        if isinstance(pix[0], int):
            if [(pix[0] + movement), pix[1]] in occupied:
                return block
            elif (pix[0] + movement) >= W_H or (pix[0] + movement) < 0:
                return block

    for pix in block:
        if isinstance(pix[0], int):
            rect = pygame.Rect(pix[0], pix[1], blockSize, blockSize)
            WINDOW.fill(BLACK, rect)

    for pix in block:
        if isinstance(pix[0], int):
            rect = pygame.Rect((pix[0] + movement), pix[1], blockSize, blockSize)
            old.append([(pix[0] + movement), pix[1]])
            WINDOW.fill(SELECTED_color, rect)

    draw_grid(WINDOW)
    return old


def change_shape(WINDOW, block, b_type, state):
    """Let user change shape if possible"""
    istate = state
    qwe = 0
    for p in b_type[state]:
        if p == 1:
            val = qwe
            break
        qwe += 1

    start = [(int(block[0][0]) - (blockSize * val)), block[0][1]]
    maxi = len(b_type)
    if state == (maxi - 1):
        state = 0
    else:
        state += 1

    new_shape = b_type[state]
    x = start[0]
    y = start[1]
    _X = x
    x__ = x
    __x = x
    _Y = y
    y__ = y
    row = 4

    for pix in new_shape:
        if pix == 0:
            pass
        else:
            if [x__, y__] in occupied or x__ >= W_H or x__ < 0 or y__ >= W_H:
                return block, istate
        row -= 1
        x__ += blockSize
        if row == 0:
            y__ += blockSize
            x__ = __x
            row = 4

    row = 4

    for coord in block:
        if isinstance(coord[0], int):
            rect = pygame.Rect(int(coord[0]), coord[1], blockSize, blockSize)
            WINDOW.fill(BLACK, rect)

    for value in new_shape:
        if value == 0:
            pass
        else:
            rect = pygame.Rect(x, y, blockSize, blockSize)
            WINDOW.fill(SELECTED_color, rect)
        row -= 1
        x += blockSize
        if row == 0:
            y += blockSize
            x = _X
            row = 4

    old = []
    plus = 0
    _plus = 0
    for p in new_shape:
        if p == 1:
            old.append([(_X + plus), (_Y + _plus)])
        else:
            old.append([str((_X + plus)), (_Y + _plus)])
        plus += blockSize
        if plus == (4 * blockSize):
            _plus += blockSize
            plus = 0

    draw_grid(WINDOW)
    return old, state


# Default speed and controls
SPEED = 60
LEFT = K_a
RIGHT = K_d
DOWN = K_s
CHANGE_SH = K_w


def handle_input(WINDOW, block, not_moving, block_types, state):
    """Respond to user input with functions"""
    time_end = time.time() + (blockSize / SPEED)  # Speed
    run = True

    while time_end > time.time():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == CHANGE_SH:
                    block, state = change_shape(WINDOW, block, block_types, state)
                if event.key == K_ESCAPE:
                    return 0, 0, 0, 0

        time.sleep(0.1)
        key_presses = pygame.key.get_pressed()

        if key_presses[LEFT]:  # Left
            block = move_x_axis(WINDOW, block, -1)
        elif key_presses[RIGHT]:  # Right
            block = move_x_axis(WINDOW, block, +1)
        elif key_presses[DOWN]:  # Down
            block, not_moving = move_y_axis(WINDOW, block)

        pygame.display.update()

    return block, not_moving, state, run


def check_line(WINDOW, score):
    """If last line is complete remove it and shift other blocks (y - 1)"""
    global occupied
    run = True
    new_oc = []
    for elem in occupied:
        if elem not in new_oc:
            new_oc.append(elem)

    occupied = new_oc

    y_s = []
    for entry in occupied:
        if entry[1] not in y_s:
            y_s.append(entry[1])

    new_occupied = []
    for coor in y_s:
        counter = 0
        for e in occupied:
            if e[1] == coor:
                counter += 1
            if e[1] == 0:
                run = False
                return score, run
        if counter == total_blocks:
            score += 5
            for en in occupied:
                if en[1] == coor:
                    recta = pygame.Rect(int(en[0]), en[1], blockSize, blockSize)
                    WINDOW.fill(BLACK, recta)
                    pygame.display.update()
                elif en[1] < coor:
                    new_occupied.append([int(en[0]), (en[1] + blockSize)])
                else:
                    new_occupied.append(en)

            for ento in occupied:
                rects = pygame.Rect(int(ento[0]), ento[1], blockSize, blockSize)
                WINDOW.fill(BLACK, rects)
            occupied = new_occupied
            for ento in occupied:
                rects = pygame.Rect(int(ento[0]), ento[1], blockSize, blockSize)
                WINDOW.fill(SELECTED_color, rects)
            break

    return score, run


def draw_text_on_screen(WINDOW, text, size, color, mode):
    """Draw text through a series of modes"""
    font = pygame.font.Font(retro_font, size)

    if mode == 1:
        label = font.render(text, 1, color)
        WINDOW.blit(label, (((W_H / 2) - (label.get_width() / 2)), ((W_H / 2) - (label.get_width() / 2))))
    elif mode == 2:
        label = font.render(str(text), 1, color)
        label2 = font.render("Score", 1, color)

        rect = pygame.Rect(W_H, 100, 200, 25)
        WINDOW.fill(BLACK, rect)

        WINDOW.blit(label2, (((W_H + 100) - label2.get_width() / 2), (50)))
        WINDOW.blit(label, ((W_H + 100 - label.get_width() / 2), (100)))
    elif mode == 3:
        rect = pygame.Rect(W_H + 30, 260, 200, W_H)
        WINDOW.fill(BLACK, rect)

        label = font.render("Next", 1, color)
        WINDOW.blit(label, (((W_H + 100) - label.get_width() / 2), (200)))

        bloc = text[0]
        y = 260
        x = W_H + 30
        _X = x
        row = 4

        for val in bloc:
            if val == 1:
                rect = pygame.Rect(x, y, blockSize, blockSize)
                WINDOW.fill(SELECTED_color, rect)
            row -= 1
            x += blockSize
            if row == 0:
                y += blockSize
                x = _X
                row = 4

        draw_grid(WINDOW)


def main():
    """ Manage game """
    WINDOW = pygame.display.set_mode(((W_H + 200), W_H))
    pygame.display.set_caption("Tetris")
    WINDOW.fill(BLACK)

    score = 0
    run = True
    not_moving = True  # Flag to check if block reaches floor
    next_s = random.choice([S, Z, T, O, I, J, L])

    while run:

        if not_moving == False:
            block, not_moving = move_y_axis(WINDOW, block)
        if not_moving:
            block, block_types = spawn_block(WINDOW, next_s)
            next_s = random.choice([S, Z, T, O, I, J, L])
            draw_text_on_screen(WINDOW, next_s, 25, WHITE, 3)
            state = 0
            not_moving = False

        block, not_moving, state, run = handle_input(WINDOW, block, not_moving, block_types, state)
        if block == 0 and not_moving == 0 and run == 0:
            return
        pygame.display.update()

        score, contin = check_line(WINDOW, score)
        draw_text_on_screen(WINDOW, str(score), 25, WHITE, 2)

        if contin == False:
            draw_text_on_screen(WINDOW, "You Lost!", 60, (220, 20, 60), 1)
            pygame.display.update()
            time.sleep(3)
            return

    sys.exit()


def settings_panel():
    """Gui for user to change settings"""
    global SELECTED_color
    global SPEED
    global LEFT
    global RIGHT
    global DOWN
    global CHANGE_SH
    win = pygame.display.set_mode((400, 370))
    pygame.display.set_caption("Settings")
    win.fill(BLACK)
    run = True

    font1 = pygame.font.Font(retro_font, 30)
    label1 = font1.render("Settings", 1, (255, 255, 102))
    win.blit(label1, ((400 / 2 - label1.get_width() / 2), (400 / 20)))

    font2 = pygame.font.Font(retro_font, 20)

    label_theme = font2.render("Change Theme ", 1, (255, 255, 255))
    label_speed = font2.render("Change Speed ", 1, (255, 255, 255))
    label_contr = font2.render("Change controls", 1, (255, 255, 255))

    font3 = pygame.font.Font(retro_font, 17)
    l_left = font3.render("Left", 1, (255, 255, 255))
    l_right = font3.render("Right", 1, (255, 255, 255))
    l_down = font3.render("Down", 1, (255, 255, 255))
    l_shape = font3.render("Rotate", 1, (255, 255, 255))

    left_val = font3.render(pygame.key.name(LEFT), 1, (0, 0, 0))
    right_val = font3.render(pygame.key.name(RIGHT), 1, (0, 0, 0))
    down_val = font3.render(pygame.key.name(DOWN), 1, (0, 0, 0))
    rotate_val = font3.render(pygame.key.name(CHANGE_SH), 1, (0, 0, 0))

    left_box = pygame.Rect(400 / 1.9, 400 / 1.8, left_val.get_width() + 10, 20)
    right_box = pygame.Rect(400 / 1.9, 400 / 1.58, right_val.get_width() + 10, 20)
    down_box = pygame.Rect(400 / 1.9, 400 / 1.4, down_val.get_width() + 10, 20)
    rotate_box = pygame.Rect(400 / 1.9, 400 / 1.26, rotate_val.get_width() + 10, 20)

    win.fill(WHITE, left_box)
    win.fill(WHITE, right_box)
    win.fill(WHITE, down_box)
    win.fill(WHITE, rotate_box)
    win.blit(left_val, ((400 / 1.88), (400 / 1.8)))
    win.blit(right_val, ((400 / 1.88), (400 / 1.58)))
    win.blit(down_val, ((400 / 1.88), (400 / 1.4)))
    win.blit(rotate_val, ((400 / 1.88), (400 / 1.26)))

    win.blit(l_left, ((400 / 3), (400 / 1.8)))
    win.blit(l_right, ((400 / 3.2), (400 / 1.58)))
    win.blit(l_down, ((400 / 3.1), (400 / 1.4)))
    win.blit(l_shape, ((400 / 3.64), (400 / 1.26)))

    red = pygame.Rect((400 / 1.6), (400 / 4.5), 25, 25)
    green = pygame.Rect((400 / 1.4), (400 / 4.5), 25, 25)
    blue = pygame.Rect((400 / 1.25), (400 / 4.5), 25, 25)
    white = pygame.Rect((400 / 1.125), (400 / 4.5), 25, 25)

    win.blit(label_theme, ((400 / 10), (400 / 4.5)))
    win.blit(label_speed, ((400 / 10), (400 / 3)))
    win.blit(label_contr, ((400 / 10), (400 / 2.2)))
    win.fill(RED, red)
    win.fill(GREEN, green)
    win.fill(BLUE, blue)
    win.fill(WHITE, white)

    label_spp = font2.render(str(SPEED), 1, (0, 0, 0))
    speed_box = pygame.Rect((400 / 1.6), (400 / 3), label_spp.get_width() + 5, 25)

    win.fill(WHITE, speed_box)
    win.blit(label_spp, ((400 / 1.59), (400 / 3)))

    pygame.display.update()
    click = False
    click2 = False
    active = False
    global selected_box
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE and SPEED != "":
                    return
            if not click:
                if red.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (169, 169, 169), red, 3)
                else:
                    pygame.draw.rect(win, BLACK, red, 3)
                if green.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (169, 169, 169), green, 3)
                else:
                    pygame.draw.rect(win, BLACK, green, 3)
                if blue.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (169, 169, 169), blue, 3)
                else:
                    pygame.draw.rect(win, BLACK, blue, 3)
                if white.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (169, 169, 169), white, 3)
                else:
                    pygame.draw.rect(win, BLACK, white, 3)

                pygame.display.update()
            if not click2:
                if left_box.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, RED, left_box, 3)
                else:
                    pygame.draw.rect(win, BLACK, left_box, 3)
                if right_box.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, RED, right_box, 3)
                else:
                    pygame.draw.rect(win, BLACK, right_box, 3)
                if down_box.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, RED, down_box, 3)
                else:
                    pygame.draw.rect(win, BLACK, down_box, 3)
                if rotate_box.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, RED, rotate_box, 3)
                else:
                    pygame.draw.rect(win, BLACK, rotate_box, 3)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if red.collidepoint(pygame.mouse.get_pos()):
                    click = True
                    pygame.draw.rect(win, BLACK, white, 3)
                    pygame.draw.rect(win, BLACK, blue, 3)
                    pygame.draw.rect(win, BLACK, green, 3)

                    pygame.draw.rect(win, (169, 169, 169), red, 3)
                    SELECTED_color = RED
                elif green.collidepoint(pygame.mouse.get_pos()):
                    click = True
                    pygame.draw.rect(win, BLACK, white, 3)
                    pygame.draw.rect(win, BLACK, blue, 3)
                    pygame.draw.rect(win, BLACK, red, 3)

                    pygame.draw.rect(win, (169, 169, 169), green, 3)
                    SELECTED_color = GREEN
                elif blue.collidepoint(pygame.mouse.get_pos()):
                    click = True
                    pygame.draw.rect(win, BLACK, green, 3)
                    pygame.draw.rect(win, BLACK, red, 3)
                    pygame.draw.rect(win, BLACK, white, 3)

                    pygame.draw.rect(win, (169, 169, 169), blue, 3)
                    SELECTED_color = BLUE
                elif white.collidepoint(pygame.mouse.get_pos()):
                    click = True
                    pygame.draw.rect(win, BLACK, blue, 3)
                    pygame.draw.rect(win, BLACK, green, 3)
                    pygame.draw.rect(win, BLACK, red, 3)

                    pygame.draw.rect(win, (169, 169, 169), white, 3)
                    SELECTED_color = WHITE
                else:
                    click = False

                if speed_box.collidepoint(pygame.mouse.get_pos()):
                    active = True
                    pygame.draw.rect(win, RED, speed_box, 3)
                else:
                    pygame.draw.rect(win, BLACK, speed_box, 3)
                    active = False

                if left_box.collidepoint(pygame.mouse.get_pos()):
                    click2 = True
                    pygame.draw.rect(win, BLACK, right_box, 3)
                    pygame.draw.rect(win, BLACK, down_box, 3)
                    pygame.draw.rect(win, BLACK, rotate_box, 3)

                    pygame.draw.rect(win, RED, left_box, 3)
                    selected_box = left_box
                elif right_box.collidepoint(pygame.mouse.get_pos()):
                    click2 = True
                    pygame.draw.rect(win, BLACK, left_box, 3)
                    pygame.draw.rect(win, BLACK, down_box, 3)
                    pygame.draw.rect(win, BLACK, rotate_box, 3)

                    pygame.draw.rect(win, RED, right_box, 3)
                    selected_box = right_box
                elif down_box.collidepoint(pygame.mouse.get_pos()):
                    click2 = True
                    pygame.draw.rect(win, BLACK, right_box, 3)
                    pygame.draw.rect(win, BLACK, left_box, 3)
                    pygame.draw.rect(win, BLACK, rotate_box, 3)

                    pygame.draw.rect(win, RED, down_box, 3)
                    selected_box = down_box
                elif rotate_box.collidepoint(pygame.mouse.get_pos()):
                    click2 = True
                    pygame.draw.rect(win, BLACK, right_box, 3)
                    pygame.draw.rect(win, BLACK, down_box, 3)
                    pygame.draw.rect(win, BLACK, left_box, 3)

                    pygame.draw.rect(win, RED, rotate_box, 3)
                    selected_box = rotate_box
                else:
                    click2 = False
                pygame.display.update()

            if click2:
                if event.type == pygame.KEYDOWN:
                    try:
                        if selected_box == left_box:
                            print(pygame.key.name(event.key))
                            win.fill(BLACK, left_box)
                            pygame.draw.rect(win, BLACK, left_box, 3)
                            LEFT = event.key
                            left_val = font3.render(pygame.key.name(event.key), 1, (0, 0, 0))
                            left_box = pygame.Rect(400 / 1.9, 400 / 1.8, left_val.get_width() + 10, 20)
                            selected_box = left_box
                            win.fill(WHITE, left_box)
                            win.blit(left_val, ((400 / 1.88), (400 / 1.8)))
                            pygame.draw.rect(win, RED, left_box, 3)

                        elif selected_box == right_box:
                            win.fill(BLACK, right_box)
                            pygame.draw.rect(win, BLACK, right_box, 3)
                            RIGHT = event.key
                            right_val = font3.render(pygame.key.name(event.key), 1, (0, 0, 0))
                            right_box = pygame.Rect(400 / 1.9, 400 / 1.58, right_val.get_width() + 10, 20)
                            selected_box = right_box
                            win.fill(WHITE, right_box)
                            win.blit(right_val, ((400 / 1.88), (400 / 1.58)))
                            pygame.draw.rect(win, RED, right_box, 3)

                        elif selected_box == down_box:
                            win.fill(BLACK, down_box)
                            pygame.draw.rect(win, BLACK, down_box, 3)
                            DOWN = event.key
                            down_val = font3.render(pygame.key.name(event.key), 1, (0, 0, 0))
                            down_box = pygame.Rect(400 / 1.9, 400 / 1.4, down_val.get_width() + 10, 20)
                            selected_box = down_box
                            win.fill(WHITE, down_box)
                            win.blit(down_val, ((400 / 1.88), (400 / 1.4)))
                            pygame.draw.rect(win, RED, down_box, 3)

                        elif selected_box == rotate_box:
                            win.fill(BLACK, rotate_box)
                            pygame.draw.rect(win, BLACK, rotate_box, 3)
                            CHANGE_SH = event.key
                            rotate_val = font3.render(pygame.key.name(event.key), 1, (0, 0, 0))
                            rotate_box = pygame.Rect(400 / 1.9, 400 / 1.26, rotate_val.get_width() + 10, 20)
                            selected_box = rotate_box
                            win.fill(WHITE, rotate_box)
                            win.blit(rotate_val, ((400 / 1.88), (400 / 1.26)))
                            pygame.draw.rect(win, RED, rotate_box, 3)

                    except:
                        pass

                    pygame.display.update()

            if active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        try:
                            SPEED = int(str(SPEED)[:-1])
                        except:
                            SPEED = ""
                        pygame.draw.rect(win, BLACK, speed_box, 3)
                    try:
                        if int(event.unicode) in range(0, 10):
                            SPEED = int(str(SPEED) + event.unicode)
                            pygame.draw.rect(win, BLACK, speed_box, 3)
                    except:
                        pass

                win.fill(BLACK, speed_box)
                label_spp = font2.render(str(SPEED), 1, (0, 0, 0))
                speed_box = pygame.Rect((400 / 1.6), (400 / 3), label_spp.get_width() + 5, 25)

                win.fill(WHITE, speed_box)
                win.blit(label_spp, ((400 / 1.59), (400 / 3)))
                pygame.draw.rect(win, RED, speed_box, 3)
                pygame.display.update()


def help_screen():
    """Help screen to tell present controls"""
    while True:
        win = pygame.display.set_mode((400, 300))
        pygame.display.set_caption("Help")
        win.fill(BLACK)

        font1 = pygame.font.Font(retro_font, 30)
        label1 = font1.render("Help", 1, WHITE)
        win.blit(label1, ((400 / 2 - label1.get_width() / 2), (400 / 100)))
        pygame.draw.line(win, WHITE, (0, 45), (400, 45))

        font2 = pygame.font.Font(retro_font, 12)
        label2 = font2.render("Tetris v1.0 ~ Aditya Gaur", 1, (255, 127, 80))
        win.blit(label2, ((400 / 2 - label2.get_width() / 2), (300 / 1.08)))

        font3 = pygame.font.Font(retro_font, 20)
        label3 = font3.render("Move Left ", 1, WHITE)
        label4 = font3.render("Move Right ", 1, WHITE)
        label5 = font3.render("Move Down ", 1, WHITE)
        label6 = font3.render("Change Shape ", 1, WHITE)
        label7 = pygame.font.Font(retro_font, 16).render("Press Esc to return to main menu", 1, BLUE)

        win.blit(label3, ((400 / 14), (400 / 6)))
        win.blit(label4, ((400 / 14), (400 / 4.04)))
        win.blit(label5, ((400 / 14), (400 / 3.05)))
        win.blit(label6, ((400 / 14), (400 / 2.45)))
        win.blit(label7, ((400 / 2 - label7.get_width() / 2), (400 / 1.9)))

        left_val = font3.render(pygame.key.name(LEFT), 1, (0, 0, 0))
        right_val = font3.render(pygame.key.name(RIGHT), 1, (0, 0, 0))
        down_val = font3.render(pygame.key.name(DOWN), 1, (0, 0, 0))
        rotate_val = font3.render(pygame.key.name(CHANGE_SH), 1, (0, 0, 0))

        left_box = pygame.Rect(400 / 1.5, 400 / 6, left_val.get_width() + 10, 20)
        right_box = pygame.Rect(400 / 1.5, 400 / 4.04, right_val.get_width() + 10, 20)
        down_box = pygame.Rect(400 / 1.5, 400 / 3.05, down_val.get_width() + 10, 20)
        rotate_box = pygame.Rect(400 / 1.5, 400 / 2.45, rotate_val.get_width() + 10, 20)

        win.fill(WHITE, left_box)
        win.fill(WHITE, right_box)
        win.fill(WHITE, down_box)
        win.fill(WHITE, rotate_box)
        win.blit(left_val, ((400 / 1.48), (400 / 6.2)))
        win.blit(right_val, ((400 / 1.48), (400 / 4.14)))
        win.blit(down_val, ((400 / 1.48), (400 / 3.13)))
        win.blit(rotate_val, ((400 / 1.48), (400 / 2.5)))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    return


def main_screen():
    """Main screen to navigate through the game"""
    while True:
        run = True
        win = pygame.display.set_mode((300, 300))
        pygame.display.set_caption("Tetris")
        bg = pygame.image.load(bg_jpg)
        bg = pygame.transform.scale(bg, (300, 300))
        win.blit(bg, (0, 0))

        font1 = pygame.font.Font(retro_font, 30)
        label1 = font1.render("Tetris", 1, (255, 255, 102))
        win.blit(label1, ((300 / 2 - label1.get_width() / 2), (300 / 20)))

        font2 = pygame.font.Font(retro_font, 20)
        label_start = font2.render("Start Game", 1, (255, 255, 255))
        label_setting = font2.render("Settings", 1, (255, 255, 255))
        label_help = font2.render("Help", 1, (255, 255, 255))

        start_button = pygame.Rect((300 / 2 - label_start.get_width() / 2), (300 / 3), label_start.get_width(), 25)
        win.fill(BLACK, start_button)

        settings = pygame.Rect((300 / 2 - label_setting.get_width() / 2), (300 / 2.4), label_setting.get_width(), 25)
        win.fill(BLACK, settings)

        help_b = pygame.Rect((300 / 2 - label_help.get_width() / 2), (300 / 2), label_help.get_width(), 25)
        win.fill(BLACK, help_b)

        win.blit(label_start, ((300 / 2 - label_start.get_width() / 2), (300 / 3)))
        win.blit(label_setting, ((300 / 2 - label_setting.get_width() / 2), (300 / 2.4)))
        win.blit(label_help, ((300 / 2 - label_help.get_width() / 2), (300 / 2)))
        pygame.display.update()

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (220, 20, 60), start_button, 2)
                else:
                    pygame.draw.rect(win, BLACK, start_button, 2)
                if settings.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (220, 20, 60), settings, 2)
                else:
                    pygame.draw.rect(win, BLACK, settings, 2)
                if help_b.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(win, (220, 20, 60), help_b, 2)
                else:
                    pygame.draw.rect(win, BLACK, help_b, 2)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(pygame.mouse.get_pos()):
                        global occupied
                        occupied = []
                        main()
                        run = False
                    elif settings.collidepoint(pygame.mouse.get_pos()):
                        settings_panel()
                        run = False
                    elif help_b.collidepoint(pygame.mouse.get_pos()):
                        help_screen()
                        run = False


if __name__ == '__main__':
    main_screen()
