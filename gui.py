import pygame, sys, random, time
from pygame.locals import QUIT, KEYDOWN, MOUSEBUTTONDOWN

import astar

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('A* pathfinder')
clock = pygame.time.Clock()
FPS = 250

GRID_SIZES = (HEIGHT, WIDTH // 1.2)
GRID_COORS = (0, 0)
GRID_DIMENSIONS = (50, 50)
g = astar.Grid(GRID_DIMENSIONS)
g.coefficient = 1

NODE_WIDTH, NODE_HEIGHT = GRID_SIZES[1] // GRID_DIMENSIONS[1], GRID_SIZES[0] // GRID_DIMENSIONS[0]
graphical_grid = [[None for _ in range(GRID_DIMENSIONS[1])] for _ in range(GRID_DIMENSIONS[0])]

def assign_node_coors():
    """Assigns coordinates to nodes in grid"""
    for j in range(GRID_DIMENSIONS[0]):
        for i in range(GRID_DIMENSIONS[1]):
            graphical_grid[j][i] = pygame.Rect(i * NODE_WIDTH, j * NODE_HEIGHT, NODE_WIDTH - 1, NODE_HEIGHT - 1)

def draw_grid():
    for j in range(GRID_DIMENSIONS[0]):
        for i in range(GRID_DIMENSIONS[1]):
            pygame.draw.rect(screen, g.grid[j][i].color, graphical_grid[j][i])


def find_node():
    """Locates the coordinates of node at given mouse position"""
    mx, my = pygame.mouse.get_pos()
    if mx < GRID_SIZES[1] and my < GRID_SIZES[0]:
        cur_y, cur_x = 0, 0
        j, i = 0, 0

        while j < GRID_DIMENSIONS[0] - 1:
            cur_y += NODE_HEIGHT
            j += 1
            if cur_y > my:
                cur_y -= my
                j -= 1
                break

        while i < GRID_DIMENSIONS[1] - 1:
            cur_x += NODE_WIDTH
            i += 1
            if cur_x > mx:
                cur_x -= mx
                i -= 1
                break
        return g.grid[j][i]

assign_node_coors()


def main():
    while True:
        clock.tick(FPS)

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                main()

        screen.fill((0, 0, 0))
        draw_grid()

        if not g.finished:
            start_time = time.time()
            while not g.finished:
                g.next()
            else:
                print(time.time() - start_time)

        pygame.display.update()


def main_paused():
        while True:
            clock.tick(200)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN:
                    main()
                if pygame.mouse.get_pressed()[0]:
                    find_node().make_unwalkable()
                elif pygame.mouse.get_pressed()[2]:
                    find_node().make_walkable()

            screen.fill((0, 0, 0))
            draw_grid()
            pygame.display.update()


def main_get_start_end():
        screen.fill((0, 0, 0))
        draw_grid()
        pygame.display.update()
        g.start_pos = ()
        g.end_pos = ()
        while True:
            clock.tick(200)

            events = pygame.event.get()
            for event in events:
                if event.type == QUIT:
                    sys.exit()
                if pygame.mouse.get_pressed()[0]:
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
                g.initialize()
                main_paused()

            screen.fill((0, 0, 0))
            draw_grid()
            pygame.display.update()


main_get_start_end()