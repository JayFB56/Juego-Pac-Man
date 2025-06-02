# Crear un nuevo archivo con el código completo corregido (parte 1 de 2)
#corrected_code_part1 =
# pacman_game_fixed.py - Parte 1
import pygame
import pygame.freetype
import math
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman con Menú")
clock = pygame.time.Clock()

FONT = pygame.freetype.SysFont("Comic Sans MS", 32)
BIG_FONT = pygame.freetype.SysFont("Comic Sans MS", 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
VULNERABLE_COLOR = (33, 33, 255)
BLINK_COLORS = [(33, 33, 255), (255, 255, 255)]

input_box = pygame.Rect(300, 250, 200, 50)
button_rect = pygame.Rect(350, 350, 100, 50)

alias = ""
alias_error = False
active_input = False

def load_ghost_images():
    ghost_images = {}
    try:
        ghost_images['red'] = pygame.image.load('rojo.png').convert_alpha()
        ghost_images['pink'] = pygame.image.load('rosa.png').convert_alpha()
        ghost_images['orange'] = pygame.image.load('naranja.png').convert_alpha()
        for color in ghost_images:
            ghost_images[color] = pygame.transform.scale(ghost_images[color], (20, 20))
        ghost_images['vulnerable'] = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(ghost_images['vulnerable'], VULNERABLE_COLOR, [0, 0, 20, 20])
        blink1 = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(blink1, WHITE, [0, 0, 20, 20])
        ghost_images['blink'] = [ghost_images['vulnerable'], blink1]
        return ghost_images
    except:
        return None

ghost_images = load_ghost_images()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Block(pygame.sprite.Sprite):
    def __init__(self, color, w, h, special=False):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, w, h])
        self.rect = self.image.get_rect()
        self.is_special = special
"""

# Guardar el archivo parte 1
file_path_part1 = "/mnt/data/pacman_game_fixed_part1.py"
with open(file_path_part1, "w", encoding="utf-8") as f:
    f.write(corrected_code_part1)

file_path_part1
# Crear un nuevo archivo con el código completo corregido (parte 1 de 2)
corrected_code_part1 = """
# pacman_game_fixed.py - Parte 1
import pygame
import pygame.freetype
import math
import random
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman con Menú")
clock = pygame.time.Clock()

FONT = pygame.freetype.SysFont("Comic Sans MS", 32)
BIG_FONT = pygame.freetype.SysFont("Comic Sans MS", 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
VULNERABLE_COLOR = (33, 33, 255)
BLINK_COLORS = [(33, 33, 255), (255, 255, 255)]

input_box = pygame.Rect(300, 250, 200, 50)
button_rect = pygame.Rect(350, 350, 100, 50)

alias = ""
alias_error = False
active_input = False

def load_ghost_images():
    ghost_images = {}
    try:
        ghost_images['red'] = pygame.image.load('rojo.png').convert_alpha()
        ghost_images['pink'] = pygame.image.load('rosa.png').convert_alpha()
        ghost_images['orange'] = pygame.image.load('naranja.png').convert_alpha()
        for color in ghost_images:
            ghost_images[color] = pygame.transform.scale(ghost_images[color], (20, 20))
        ghost_images['vulnerable'] = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(ghost_images['vulnerable'], VULNERABLE_COLOR, [0, 0, 20, 20])
        blink1 = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(blink1, WHITE, [0, 0, 20, 20])
        ghost_images['blink'] = [ghost_images['vulnerable'], blink1]
        return ghost_images
    except:
        return None

ghost_images = load_ghost_images()

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Block(pygame.sprite.Sprite):
    def __init__(self, color, w, h, special=False):
        super().__init__()
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, color, [0, 0, w, h])
        self.rect = self.image.get_rect()
        self.is_special = special
"""

# Guardar el archivo parte 1
file_path_part1 = "/mnt/data/pacman_game_fixed_part1.py"
with open(file_path_part1, "w", encoding="utf-8") as f:
    f.write(corrected_code_part1)

file_path_part1
# Crear la tercera parte del código corregido con el resto de la lógica del juego
corrected_code_part3 = """
def setup_walls(sprites):
    wall_list = pygame.sprite.Group()
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
    for x, y, w, h in walls:
        wall = Wall(x, y, w, h)
        wall_list.add(wall)
        sprites.add(wall)
    return wall_list

def setup_gate(sprites):
    gate = pygame.sprite.Group()
    gate_wall = Wall(282, 242, 42, 2)
    gate.add(gate_wall)
    sprites.add(gate_wall)
    return gate

def create_game():
    all_sprites_list = pygame.sprite.Group()
    wall_list = setup_walls(all_sprites_list)
    gate = setup_gate(all_sprites_list)

    player = Player(300, 400)
    all_sprites_list.add(player)

    pellet_list = pygame.sprite.Group()
    for row in range(15):
        for col in range(15):
            if (row, col) not in [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7)]:
                pellet = Block(YELLOW, 12, 12)
                pellet.rect.centerx = (col * 40) + 20
                pellet.rect.centery = (row * 40) + 20
                if not any(pellet.rect.colliderect(w.rect) for w in wall_list):
                    pellet_list.add(pellet)
                    all_sprites_list.add(pellet)

    special_pellets = pygame.sprite.Group()
    positions = [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7), (7, 7), (7, 8), (7, 9)]
    for row, col in positions:
        pellet = Block(WHITE, 16, 16, special=True)
        pellet.rect.centerx = (col * 40) + 20
        pellet.rect.centery = (row * 40) + 20
        if not any(pellet.rect.colliderect(w.rect) for w in wall_list):
            special_pellets.add(pellet)
            all_sprites_list.add(pellet)

    ghost_list = pygame.sprite.Group()
    ghost_types = ['red', 'pink', 'orange']
    ghost_positions = [(150, 200), (300, 200), (450, 200)]
    for ghost_type, pos in zip(ghost_types, ghost_positions):
        ghost = Ghost(ghost_type, pos[0], pos[1])
        ghost_list.add(ghost)
        all_sprites_list.add(ghost)

    return all_sprites_list, wall_list, gate, player, pellet_list, ghost_list, special_pellets

def draw_menu():
    screen.fill(LIGHT_BLUE)
    BIG_FONT.render_to(screen, (220, 100), "¡Bienvenido a Pacman!", BLACK)
    FONT.render_to(screen, (270, 200), "Ingresa tu alias:", BLACK)
    pygame.draw.rect(screen, WHITE, input_box, border_radius=5)
    pygame.draw.rect(screen, BLACK, input_box, 2, border_radius=5)
    FONT.render_to(screen, (input_box.x + 10, input_box.y + 10), alias, BLACK)
    pygame.draw.rect(screen, (0, 200, 0), button_rect, border_radius=5)
    FONT.render_to(screen, (button_rect.x + 10, button_rect.y + 10), "Jugar", WHITE)
    if alias_error:
        FONT.render_to(screen, (250, 420), "¡Ingresa un alias para jugar!", RED)

def show_message(text):
    font = pygame.font.SysFont('Arial', 36)
    message = font.render(text, True, WHITE)
    rect = message.get_rect(center=(400, 300))
    screen.blit(message, rect)


# Guardar la tercera parte como archivo
file_path_part3 = "/mnt/data/pacman_game_fixed_part3.py"
with open(file_path_part3, "w", encoding="utf-8") as f:
    f.write(corrected_code_part3)

file_path_part3
