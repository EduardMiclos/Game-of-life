'''
In memory of John Horton Conway.
With love, by Micloș Eduard-Pavel.

The game of life - rules:

1. Any live cell with fewer than two life neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''

# ----- IMPORTS -----
import sys
import pygame as pg
import numpy as np
# ------------------




# ----- GLOBAL VARIABLES -----

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1300
SCREEN = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
TITLE = 'Game of life'

BG_COLOR = (59, 59, 58)
RECT_COLORS = [(66, 183, 255), (138, 138, 138)]
BUTTON_COLORS = [(142, 237, 123), (226, 237, 123)]

RECT_SIZE = 10
STATE_TEXT_FONT_SIZE = 50
POPULATION_TEXT_FONT_SIZE = 20
BUTTON_HEIGHT = 60

CLOCK = pg.time.Clock()
CELLS = []
NEXT_STATE = []

DEAD_STATE = 1
ALIVE_STATE = 0

GAME_TIME = 0
START = 0
POPULATION = 0
# ----------------------------




# ----- FUNCTIONS -----
def set_game_title():
    pg.display.set_caption(TITLE)

def set_screen_background():
    SCREEN.fill(BG_COLOR)

def initialize_world():
    global CELLS, NEXT_STATE
    CELLS = np.ones((int((WINDOW_HEIGHT - BUTTON_HEIGHT)/RECT_SIZE) + 3, int(WINDOW_WIDTH/RECT_SIZE) + 2), dtype=int)
    NEXT_STATE = np.copy(CELLS)

def update_grid():
    global POPULATION
    POPULATION = 0

    for i in range(int((WINDOW_HEIGHT - BUTTON_HEIGHT)/RECT_SIZE)):
        for j in range(int(WINDOW_WIDTH/RECT_SIZE) + 1):
            cls = CELLS[i + 1][j + 1]
            if cls == ALIVE_STATE:
                POPULATION += 1
            pg.draw.rect(SCREEN, RECT_COLORS[cls], pg.Rect(RECT_SIZE*j, RECT_SIZE*i, RECT_SIZE, RECT_SIZE), cls)

def within_start_range(pos):
    return (pos[1] > WINDOW_HEIGHT - BUTTON_HEIGHT and pos[1] < WINDOW_HEIGHT)

def generate_cell(pos):
    global CELLS, NEXT_STATE
    X = int(pos[1] / RECT_SIZE)
    Y = int(pos[0] / RECT_SIZE)
    CELLS[X + 1][Y + 1] = ALIVE_STATE
    NEXT_STATE = np.copy(CELLS)

def kill_cell(pos):
    global CELLS, NEXT_STATE
    X = int(pos[1] / RECT_SIZE)
    Y = int(pos[0] / RECT_SIZE)
    CELLS[X + 1][Y + 1] = DEAD_STATE
    NEXT_STATE = np.copy(CELLS)

def number_of_neighbours(i, j):
    N = 0

    for k in range(-1, 2):
        for l in range(-1, 2):
            if k != 0 or l != 0:
                N += CELLS[i - k][j - l]

    return 8 - N

def create_button():
    left = 0
    top = WINDOW_HEIGHT - BUTTON_HEIGHT
    width = WINDOW_WIDTH
    height = top

    pg.draw.rect(SCREEN, BUTTON_COLORS[START], pg.Rect(left, top, width, height), 0)
    state_font = pg.font.SysFont('cambria', STATE_TEXT_FONT_SIZE)
    state_font.set_bold(3)

    population_font = pg.font.SysFont('cambria', POPULATION_TEXT_FONT_SIZE)
    population_font.set_bold(3)

    STATE_TEXT = 'START' if not START else 'PAUSE'
    POPULATION_TEXT = 'POPULATION: ' + str(POPULATION)
    SCREEN.blit(state_font.render(STATE_TEXT, True, (255, 255, 255)), (width/2 - STATE_TEXT_FONT_SIZE*2 - 10, top))
    SCREEN.blit(population_font.render(POPULATION_TEXT, True, (255, 255, 255)), (width/2 + 100, top + 20))


def Conway():
    global CELLS, NEXT_STATE
    for i in range(1, int((WINDOW_HEIGHT - BUTTON_HEIGHT)/RECT_SIZE) + 1):
        for j in range(1, int(WINDOW_WIDTH/RECT_SIZE) + 1):
            N = number_of_neighbours(i, j)
            if N < 2 or N > 3:
                NEXT_STATE[i][j] = DEAD_STATE
            elif N == 3:
                NEXT_STATE[i][j] = ALIVE_STATE

    CELLS = np.copy(NEXT_STATE)

# ---------------------




# ----- MAIN -----
initialize_world()
pg.font.init()

is_drawing = False
is_deleting = False

while True:
    set_game_title()
    set_screen_background()
    create_button()
    update_grid()
    pos = pg.mouse.get_pos()

    if is_drawing:
            generate_cell(pos)
    if is_deleting:
            kill_cell(pos)

    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if within_start_range(pos):
                    START ^= 1
                    is_drawing = False
                else:
                    is_drawing = True
            elif event.button == 3:
                if not within_start_range(pos):
                    is_deleting = True
                is_drawing = False

        elif event.type == pg.MOUSEBUTTONUP:
            is_drawing = False
            is_deleting = False

        if event.type == pg.QUIT:
            sys.exit()

    if(START):
        Conway()
        CLOCK.tick(5)
    else:
        CLOCK.tick(30)

    GAME_TIME += 100
    pg.display.update()
# ----------------
