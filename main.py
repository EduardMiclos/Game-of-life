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
import pygame.font

WINDOW = 780
GRID_SIZE = 690
SCREEN = pg.display.set_mode((GRID_SIZE, WINDOW))
TITLE = 'Game of life'


BG_COLOR = (59, 59, 58)
RECT_COLORS = [(66, 183, 255), (138, 138, 138)]
BUTTON_COLORS = [(142, 237, 123), (226, 237, 123)]

RECT_SIZE = 30
FONT_SIZE = 50

CLOCK = pg.time.Clock()
CELLS = []
NEXT_STATE = []

DEAD_STATE = 1
ALIVE_STATE = 0

GAME_TIME = 0
START = 0
# ----------------------------




# ----- FUNCTIONS -----
def set_game_title():
    pg.display.set_caption(TITLE)

def set_screen_background():
    SCREEN.fill(BG_COLOR)

def initialize_world():
    global CELLS, NEXT_STATE
    CELLS = np.ones((int(GRID_SIZE/RECT_SIZE) + 2, int(GRID_SIZE/RECT_SIZE) + 2), dtype=int)
    NEXT_STATE = np.copy(CELLS)

def update_grid():
    for i in range(int(GRID_SIZE/RECT_SIZE) + 1):
        for j in range(int(GRID_SIZE/RECT_SIZE) + 1):
            cls = CELLS[i + 1][j + 1]
            pg.draw.rect(SCREEN, RECT_COLORS[cls], pg.Rect(RECT_SIZE*j, RECT_SIZE*i, RECT_SIZE, RECT_SIZE), cls)

def within_start_range(pos):
    return (pos[1] > GRID_SIZE + RECT_SIZE and pos[1] < RECT_SIZE + WINDOW)

def generate_cell(pos):
    global CELLS, NEXT_STATE
    X = int(pos[1] / RECT_SIZE)
    Y = int(pos[0] / RECT_SIZE)
    CELLS[X + 1][Y + 1] = ALIVE_STATE
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
    top = GRID_SIZE + RECT_SIZE
    width = WINDOW
    height = WINDOW - GRID_SIZE

    pg.draw.rect(SCREEN, BUTTON_COLORS[START], pg.Rect(left, top, width, height), 0)
    font = pg.font.SysFont('cambria', FONT_SIZE)
    font.set_bold(3)

    if not START:
        TEXT = 'START'
    else:
        TEXT = 'PAUSE'

    SCREEN.blit(font.render(TEXT, True, (255, 255, 255)), (width/2 - FONT_SIZE*2 - 10, top))


def Conway():
    global CELLS, NEXT_STATE
    for i in range(1, int(GRID_SIZE/RECT_SIZE) + 1):
        for j in range(1, int(GRID_SIZE/RECT_SIZE) + 1):
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

while True:
    set_game_title()
    set_screen_background()
    create_button()
    update_grid()
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pg.mouse.get_pos()

                if within_start_range(pos):
                    START ^= 1
                else:
                    generate_cell(pos)

        if event.type == pg.QUIT:
            sys.exit()

    if(START):
        Conway()
        CLOCK.tick(5)
    else:
        CLOCK.tick(30)

    GAME_TIME += 1
    pg.display.update()
# ----------------