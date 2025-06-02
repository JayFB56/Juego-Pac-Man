from game import *
from constants import *
from entities import Block, Wall
import pygame


def setup_walls(sprites):
    walls = [
        [0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606],
        [300, 0, 6, 66], [60, 60, 186, 6], [360, 60, 186, 6], [60, 120, 66, 6],
        [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66], [480, 120, 66, 6],
        [540, 120, 6, 126], [120, 180, 126, 6], [120, 180, 6, 126], [360, 180, 126, 6],
        [480, 180, 6, 126], [180, 240, 6, 126], [180, 360, 246, 6], [420, 240, 6, 126],
        [240, 240, 42, 6], [324, 240, 42, 6], [240, 240, 6, 66], [240, 300, 126, 6],
        [360, 240, 6, 66], [0, 300, 66, 6], [540, 300, 66, 6], [60, 360, 66, 6],
        [60, 360, 6, 186], [480, 360, 66, 6], [540, 360, 6, 186], [120, 420, 366, 6],
        [120, 420, 6, 66], [480, 420, 6, 66], [180, 480, 246, 6], [300, 480, 6, 66],
        [120, 540, 126, 6], [360, 540, 126, 6]
    ]
    wall_list = pygame.sprite.Group()
    for x, y, w, h in walls:
        wall = Wall(x, y, w, h)
        wall_list.add(wall)
        sprites.add(wall)
    return wall_list


def setup_gate(sprites):
    gate_wall = Wall(282, 242, 42, 2)
    gate = pygame.sprite.Group()
    gate.add(gate_wall)
    sprites.add(gate_wall)
    return gate


def setup_pellets(sprites, walls):
    pellet_list = pygame.sprite.Group()
    special_list = pygame.sprite.Group()

    for row in range(15):
        for col in range(15):
            if (row, col) not in [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7)]:
                pellet = Block(YELLOW, 12, 12)
                pellet.rect.centerx = (col * 40) + 20
                pellet.rect.centery = (row * 40) + 20
                if not any(pellet.rect.colliderect(w.rect) for w in walls):
                    pellet_list.add(pellet)
                    sprites.add(pellet)

    special_positions = [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7)]
    for row, col in special_positions:
        color = RED if (row, col) == (5, 9) else WHITE
        pellet = Block(color, 16, 16, special=True)
        pellet.rect.centerx = (col * 40) + 20
        pellet.rect.centery = (row * 40) + 20

        if not any(pellet.rect.colliderect(w.rect) for w in walls):
            special_list.add(pellet)
            sprites.add(pellet)

        if color == RED:
            print("🔴 Bolita ROJA para disparo en:", pellet.rect.center)

    return pellet_list, special_list
