import pygame
from pygame import freetype
from constants import *

class Menu:
    def __init__(self):
        self.alias = ""
        self.active_input = False
        self.alias_error = False
        self.font = freetype.SysFont("Comic Sans MS", 32)
        self.big_font = freetype.SysFont("Comic Sans MS", 48)
        self.input_box = pygame.Rect(300, 250, 200, 50)
        self.button_rect = pygame.Rect(350, 350, 100, 50)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active_input = True
                else:
                    self.active_input = False
                if self.button_rect.collidepoint(event.pos):
                    if self.alias.strip() == "":
                        self.alias_error = True
                    else:
                        self.alias_error = False
                        return True  # señal de que se debe iniciar el juego

            elif event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_BACKSPACE:
                    self.alias = self.alias[:-1]
                elif len(self.alias) < 15:
                    self.alias += event.unicode
        return False

    def draw(self, screen):
        screen.fill(LIGHT_BLUE)
        self.big_font.render_to(screen, (70, 80), "¡Bienvenido a Pacman!", BLACK)
        self.font.render_to(screen, (180, 180), "Ingresa tu alias:", BLACK)

        self.input_box = pygame.Rect(203, 230, 200, 50)  # centrado
        self.button_rect = pygame.Rect(253, 320, 100, 50)  # centrado

        pygame.draw.rect(screen, WHITE, self.input_box, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.input_box, 2, border_radius=5)
        self.font.render_to(screen, (self.input_box.x + 10, self.input_box.y + 10), self.alias, BLACK)

        pygame.draw.rect(screen, (0, 200, 0), self.button_rect, border_radius=5)
        self.font.render_to(screen, (self.button_rect.x + 10, self.button_rect.y + 10), "Jugar", WHITE)

        if self.alias_error:
            self.font.render_to(screen, (150, 400), "¡Ingresa un alias para jugar!", RED)
