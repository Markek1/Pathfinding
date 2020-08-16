import pygame, sys, random, time
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN, K_n, K_SPACE

import astar


def draw_all():
    screen.fill((0, 0, 0))
    draw_buttons()
    draw_grid()
    pygame.display.update()


TEXTS = {}
def assign_button_coordinates(names, start_x, start_y):
    '''Assigns each button its coordinates.
       The placement depends on the shape of BUTTON_NAMES'''

    max_j, max_i = len(names), len(names[0])
    j, i = BUTTON_SHAPE
    for j in range(max_j):
        for i in range(max_i):
            BUTTON_COORS[names[j][i]] = pygame.Rect(start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT,
                                        BUTTON_WIDTH - 2, BUTTON_HEIGHT - 2)
            TEXTS[names[j][i]] = (start_x + i * BUTTON_WIDTH, start_y + j * BUTTON_HEIGHT)


def draw_text(text, font, color, surface, coordinates):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = coordinates
    surface.blit(textobj, textrect)


def draw_buttons():
    for text, button in zip(TEXTS.keys(), BUTTON_COORS.values()):
        pygame.draw.rect(screen, BUTTON_COLOR, button)
        draw_text(text, FONT, TEXT_COLOR, screen, TEXTS[text])


def check_button_press(event):
    if event.type == KEYDOWN:
        if event.key == K_n:
            for func in BUTTON_FUNCTIONS['new']:
                func()
        elif event.key == K_SPACE:
            for func in BUTTON_FUNCTIONS['path']:
                func()
    elif event.type == MOUSEBUTTONDOWN:
        mx, my = pygame.mouse.get_pos()
        for button in BUTTON_COORS.keys():
            if BUTTON_COORS[button].collidepoint((mx, my)):
                for func in BUTTON_FUNCTIONS[button]:
                    func()
                print(button)


def assign_node_coors():
    """Assigns coordinates to nodes in grid"""
    for j in range(GRID_NODES_Y):
        for i in range(GRID_NODES_X):
            graphical_grid[j][i] = pygame.Rect(i * NODE_WIDTH, j * NODE_HEIGHT, NODE_WIDTH - 1, NODE_HEIGHT - 1)


def draw_grid():
    for j in range(GRID_NODES_Y):
        for i in range(GRID_NODES_X):
            pygame.draw.rect(screen, g.grid[j][i].color, graphical_grid[j][i])


def find_node():
    """Locates the coordinates of node at given mouse position"""
    mx, my = pygame.mouse.get_pos()
    if mx < GRID_WIDTH and my < GRID_HEIGHT:
        cur_y, cur_x = 0, 0
        j, i = 0, 0

        while j < GRID_NODES_Y - 1:
            cur_y += NODE_HEIGHT
            j += 1
            if cur_y > my:
                cur_y -= my
                j -= 1
                break

        while i < GRID_NODES_X - 1:
            cur_x += NODE_WIDTH
            i += 1
            if cur_x > mx:
                cur_x -= mx
                i -= 1
                break

        if (j, i) == g.start_pos or (j, i) == g.end_pos:
            return dumping_node
        else:
            return g.grid[j][i]

    else:
        return dumping_node


def main():
    while True:
        draw_all()

        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                sys.exit()
            check_button_press(event)

        if not g.finished:
            # start_time = time.time()
            # while not g.finished:
            g.next()
            # else:
                # print(f'{(time.time() - start_time) * 1000} ms')


def main_paused():
        while True:
            draw_all()

            clock.tick(200)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                check_button_press(event)
                if pygame.mouse.get_pressed()[0]:
                    find_node().make_unwalkable()
                elif pygame.mouse.get_pressed()[2]:
                    find_node().make_walkable()


def main_get_start_end():

        g.start_pos = ()
        g.end_pos = ()
        while True:
            draw_all()

            clock.tick(200)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                check_button_press(event)
                if event.type == MOUSEBUTTONDOWN:
                    try:
                        node = find_node()
                        if g.start_pos == ():
                            g.start_pos = (node.pos)
                            node.color = (0, 0, 255)
                        elif g.end_pos == ():
                            g.end_pos = (node.pos)
                            node.color = (0, 0, 255)
                    except:
                        pass

            if g.start_pos != () and g.end_pos != ():
                main_paused()

pygame.init()
WIDTH, HEIGHT = 700, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* pathfinder')
clock = pygame.time.Clock()
FPS = 250

GRID_WIDTH, GRID_HEIGHT = WIDTH // 1.2, HEIGHT
GRID_X, GRID_Y = 0, 0
GRID_NODES_X, GRID_NODES_Y = 40, 40
g = astar.Grid((GRID_NODES_Y, GRID_NODES_X))
g.coefficient = 1

MENU_WIDTH, MENU_HEIGHT =  WIDTH - GRID_WIDTH, HEIGHT
MENU_X, MENU_Y = GRID_WIDTH, 0

BUTTON_COLOR = (100,238,255)
BUTTON_COORS = {}
BUTTON_FUNCTIONS = {
    'new':[g.new, main_get_start_end],
    'path':[g.initialize, main]
}
BUTTON_NAMES = [['new', 'path']]
BUTTON_SHAPE = (len(BUTTON_NAMES), len(BUTTON_NAMES[0]))
BUTTON_WIDTH, BUTTON_HEIGHT = (MENU_WIDTH // 0.9) // BUTTON_SHAPE[1], HEIGHT // 15
assign_button_coordinates(BUTTON_NAMES,
               MENU_X + MENU_WIDTH // 2 - (BUTTON_WIDTH * BUTTON_SHAPE[1]) // 2,
               MENU_Y + MENU_HEIGHT // 10)

FONT = pygame.font.SysFont('bahnschrift', 12)
TEXT_COLOR = (0, 0, 0)

NODE_WIDTH, NODE_HEIGHT = GRID_WIDTH // GRID_NODES_X, GRID_HEIGHT // GRID_NODES_Y
graphical_grid = [[None for _ in range(GRID_NODES_X)] for _ in range(GRID_NODES_Y)]
# used when a Node method needs to not be done on any node in the grid
dumping_node = astar.Node((GRID_NODES_X + 1, GRID_NODES_Y + 1))

assign_node_coors()
main_get_start_end()