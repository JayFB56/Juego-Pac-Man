
from pygame import time
# pacman_fixed.py
import pygame
import pygame.freetype
import math
import random
import sys

# Inicializar pygame
pygame.init()

# Pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman con Menú")
clock = pygame.time.Clock()

# Fuente
FONT = pygame.freetype.SysFont("Comic Sans MS", 32)
BIG_FONT = pygame.freetype.SysFont("Comic Sans MS", 48)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
VULNERABLE_COLOR = (33, 33, 255)
BLINK_COLORS = [(33, 33, 255), (255, 255, 255)]

# Rectángulos del menú
input_box = pygame.Rect(300, 250, 200, 50)
button_rect = pygame.Rect(350, 350, 100, 50)

# Variables de menú
alias = ""
alias_error = False
active_input = False

# Cargar imágenes de fantasmas
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

# Clases
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

class Ghost(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.color_name = color
        self.spawn_point = (x, y)
        self.direction = pygame.Vector2(2, 0)
        self.vulnerable = False
        self.vulnerable_time = 0
        self.blinking = False
        self.active = True

        if ghost_images:
            self.original_image = ghost_images[color]
        else:
            self.original_image = pygame.Surface((20, 20))
            self.original_image.fill(RED)
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, walls, gate):
        if not self.active:
            return

        current_time = pygame.time.get_ticks()
        if self.vulnerable:
            elapsed = (current_time - self.vulnerable_time) / 1000
            if elapsed > 7:
                self.end_vulnerability()
            elif elapsed > 4:
                self.blinking = True
                if ghost_images:
                    idx = int(elapsed * 5) % 2
                    self.image = ghost_images['blink'][idx]
                else:
                    self.image.fill(BLINK_COLORS[int(elapsed * 5) % 2])
            else:
                if ghost_images:
                    self.image = ghost_images['vulnerable']
                else:
                    self.image.fill(VULNERABLE_COLOR)
        else:
            if ghost_images:
                self.image = ghost_images[self.color_name]
            else:
                self.image.fill(RED)

        old = self.rect.topleft
        self.rect.x += self.direction.x
        self.rect.y += self.direction.y
        if pygame.sprite.spritecollideany(self, walls) or pygame.sprite.spritecollideany(self, gate):
            self.rect.topleft = old
            self.choose_new_direction(walls)

    def make_vulnerable(self):
        self.vulnerable = True
        self.vulnerable_time = pygame.time.get_ticks()
        if ghost_images:
            self.image = ghost_images['vulnerable']
        else:
            self.image.fill(VULNERABLE_COLOR)

    def end_vulnerability(self):
        self.vulnerable = False
        self.blinking = False

    def respawn(self):
        self.rect.center = self.spawn_point
        self.active = True
        self.end_vulnerability()

    def choose_new_direction(self, walls):
        dirs = [pygame.Vector2(2, 0), pygame.Vector2(-2, 0), pygame.Vector2(0, 2), pygame.Vector2(0, -2)]
        random.shuffle(dirs)
        for d in dirs:
            self.rect.x += d.x
            self.rect.y += d.y
            if not pygame.sprite.spritecollideany(self, walls):
                self.direction = d
                self.rect.x -= d.x
                self.rect.y -= d.y
                return
            self.rect.x -= d.x
            self.rect.y -= d.y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.radius = 20
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = 'RIGHT'
        self.change_x = 0
        self.change_y = 0
        self.mouth_opening = 0
        self.mouth_dir = 1
        self.update_image()

    def changespeed(self, x, y):
        self.change_x = x
        self.change_y = y
        if x > 0: self.direction = 'RIGHT'
        elif x < 0: self.direction = 'LEFT'
        elif y > 0: self.direction = 'DOWN'
        elif y < 0: self.direction = 'UP'

    def update(self, walls, gate):
        old = self.rect.topleft
        self.rect.x += self.change_x
        if pygame.sprite.spritecollide(self, walls, False) and not pygame.sprite.spritecollide(self, gate, False):
            self.rect.topleft = old
        old = self.rect.topleft
        self.rect.y += self.change_y
        if pygame.sprite.spritecollide(self, walls, False) and not pygame.sprite.spritecollide(self, gate, False):
            self.rect.topleft = old

        self.mouth_opening += self.mouth_dir
        if self.mouth_opening >= 10 or self.mouth_opening <= 0:
            self.mouth_dir *= -1
        self.update_image()

    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        angle = 40 * self.mouth_opening / 10
        if self.direction == 'RIGHT': sa, ea = angle, 360 - angle
        elif self.direction == 'LEFT': sa, ea = 180 + angle, 180 - angle
        elif self.direction == 'UP': sa, ea = 90 + angle, 90 - angle
        else: sa, ea = 270 + angle, 270 - angle

        points = [(self.radius, self.radius)]
        for i in range(30):
            a = math.radians(sa + (ea - sa) * i / 29)
            x = self.radius + self.radius * math.cos(a)
            y = self.radius - self.radius * math.sin(a)
            points.append((x, y))
        pygame.draw.polygon(self.image, YELLOW, points)

# Configurar laberinto
def setup_walls(sprites):
    wall_list = pygame.sprite.Group()
    walls = [
        [0, 0, 6, 600], [0, 0, 600, 6], [0, 600, 606, 6], [600, 0, 6, 606],
        [300, 0, 6, 66], [60, 60, 186, 6], [360, 60, 186, 6], [60, 120, 66, 6],
        [60, 120, 6, 126], [180, 120, 246, 6], [300, 120, 6, 66], [480, 120, 66, 6],
        [540, 120, 6, 126]
    ]
    for x, y, w, h in walls:
        wall = Wall(x, y, w, h)
        wall_list.add(wall)
        sprites.add(wall)
    return wall_list

def setup_gate(sprites):
    gate = pygame.sprite.Group()
    wall = Wall(282, 242, 42, 2)
    gate.add(wall)
    sprites.add(wall)
    return gate

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

# Función principal
def main():
    global alias, alias_error, active_input
    show_menu = True

    while True:
        if show_menu:
            draw_menu()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active_input = True
                    else:
                        active_input = False
                    if button_rect.collidepoint(event.pos):
                        if alias.strip() == "":
                            alias_error = True
                        else:
                            show_menu = False
                            alias_error = False
                elif event.type == pygame.KEYDOWN and active_input:
                    if event.key == pygame.K_BACKSPACE:
                        alias = alias[:-1]
                    elif len(alias) < 15:
                        alias += event.unicode
            clock.tick(30)
            continue

    def create_game():
        all_sprites_list = pygame.sprite.RenderPlain()
        wall_list = setupRoomOne(all_sprites_list)
        gate = setupGate(all_sprites_list)

        player = Player(300, 400)
        all_sprites_list.add(player)

        # Puntos normales (amarillos)
        pellet_list = pygame.sprite.RenderPlain()
        for row in range(15):
            for column in range(15):
                if (row, column) not in [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7)]:
                    pellet = Block(yellow, 12, 12)
                    pellet.rect.centerx = (column * 40) + 20
                    pellet.rect.centery = (row * 40) + 20
                    if not any(pellet.rect.colliderect(w.rect) for w in wall_list):
                        pellet_list.add(pellet)
                        all_sprites_list.add(pellet)

        # Puntos especiales (blancos, más grandes) - Incluyendo los 3 del centro
        special_pellets = pygame.sprite.RenderPlain()
        special_positions = [(1, 1), (1, 13), (5, 5), (5, 9), (9, 5), (9, 9), (13, 7),
                             (7, 7), (7, 8), (7, 9)]  # Añadimos las 3 bolitas del centro
        for row, column in special_positions:
            pellet = Block(white, 16, 16, is_special=True)
            pellet.rect.centerx = (column * 40) + 20
            pellet.rect.centery = (row * 40) + 20
            if not any(pellet.rect.colliderect(w.rect) for w in wall_list):
                special_pellets.add(pellet)
                all_sprites_list.add(pellet)

        # Fantasmas (usando imágenes si están disponibles)
        ghost_types = ['red', 'pink', 'orange']
        ghost_positions = [(150, 200), (300, 200), (450, 200)]
        ghost_list = pygame.sprite.RenderPlain()

        for ghost_type, pos in zip(ghost_types, ghost_positions):
            ghost = Ghost(ghost_type, pos[0], pos[1])
            ghost_list.add(ghost)
            all_sprites_list.add(ghost)

        return all_sprites_list, wall_list, gate, player, pellet_list, ghost_list, special_pellets

    def show_message(text):
        font = pygame.font.SysFont('Arial', 36)
        message = font.render(text, True, white)
        rect = message.get_rect(center=(303, 303))
        screen.blit(message, rect)

    all_sprites_list, wall_list, gate, player, pellet_list, ghost_list, special_pellets = create_game()
    game_over = False
    score = 0

    while True:
        screen.fill((0, 0, 0))
        if show_menu:
            draw_main_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active_input = True
                    else:
                        active_input = False

                    if button_rect.collidepoint(event.pos):
                        if alias.strip() == "":
                            alias_error = True
                        else:
                            alias_error = False
                            show_menu = False  # ¡Empezar el juego!

                elif event.type == pygame.KEYDOWN and active_input:
                    if event.key == pygame.K_RETURN:
                        active_input = False
                    elif event.key == pygame.K_BACKSPACE:
                        alias = alias[:-1]
                    else:
                        if len(alias) < 15:
                            alias += event.unicode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_over:
                    all_sprites_list, wall_list, gate, player, pellet_list, ghost_list, special_pellets = create_game()
                    game_over = False
                    score = 0
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        player.changespeed(-4, 0)
                    elif event.key == pygame.K_RIGHT:
                        player.changespeed(4, 0)
                    elif event.key == pygame.K_UP:
                        player.changespeed(0, -4)
                    elif event.key == pygame.K_DOWN:
                        player.changespeed(0, 4)

            elif event.type == pygame.KEYUP and not game_over:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.changespeed(0, player.change_y)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player.changespeed(player.change_x, 0)

            # Eventos de reaparición de fantasmas
            elif event.type >= pygame.USEREVENT and event.type < pygame.USEREVENT + len(ghost_list):
                ghost_index = event.type - pygame.USEREVENT
                if ghost_index < len(ghost_list.sprites()):
                    ghost_list.sprites()[ghost_index].respawn()

        if not game_over:
            player.update(wall_list, gate)
            ghost_list.update(wall_list, gate)

            # Colisión con puntos normales
            pellet_hit_list = pygame.sprite.spritecollide(player, pellet_list, True)
            for pellet in pellet_hit_list:
                score += 10

            # Colisión con puntos especiales
            special_hit_list = pygame.sprite.spritecollide(player, special_pellets, True)
            for pellet in special_hit_list:
                score += 50
                for ghost in ghost_list:
                    ghost.make_vulnerable()

            # Colisión con fantasmas
            ghost_hit_list = pygame.sprite.spritecollide(player, ghost_list, False)
            for ghost in ghost_hit_list:
                if ghost.vulnerable and ghost.active:
                    ghost.active = False
                    score += 200
                    # Reaparecer después de 5 segundos
                    pygame.time.set_timer(pygame.USEREVENT + ghost_list.sprites().index(ghost), 3000, True)
                elif not ghost.vulnerable:
                    game_over = True

        screen.fill(black)
        all_sprites_list.draw(screen)

        # Mostrar puntaje
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Puntaje: {score}", True, white)
        screen.blit(score_text, (10, 10))

        if game_over:
            show_message("Perdiste. ¿De nuevo o miedo?")

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()