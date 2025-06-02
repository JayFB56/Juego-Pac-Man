import pygame
import math
import random
from constants import *
from constants import BLINK_COLORS, VULNERABLE_COLOR

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
    def __init__(self, color, x, y, ghost_images):
        super().__init__()
        self.color_name = color
        self.spawn_point = (x, y)
        self.direction = pygame.Vector2(2, 0)
        self.vulnerable = False
        self.vulnerable_time = 0
        self.blinking = False
        self.active = True
        self.ghost_images = ghost_images

        if ghost_images:
            self.original_image = self.ghost_images[color]
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
                if self.ghost_images:
                    idx = int(elapsed * 5) % 2
                    self.image = self.ghost_images['blink'][idx]
                else:
                    self.image.fill(BLINK_COLORS[int(elapsed * 5) % 2])
            else:
                if self.ghost_images:
                    self.image = self.ghost_images['vulnerable']
                else:
                    self.image.fill(VULNERABLE_COLOR)
        else:
            if self.ghost_images:
                self.image = self.ghost_images[self.color_name]
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
        if self.ghost_images:
            self.image = self.ghost_images['vulnerable']
        else:
            self.image.fill(VULNERABLE_COLOR)

    def end_vulnerability(self):
        self.vulnerable = False
        self.blinking = False

    def respawn(self):
        self.rect.center = self.spawn_point
        self.vulnerable = False
        self.blinking = False
        self.active = True
        self.image = self.original_image.copy()

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
    def update_image(self):
        self.image.fill((0, 0, 0, 0))
        max_mouth_angle = 40
        angle = max_mouth_angle * self.mouth_opening / 10

        if self.direction == 'RIGHT':
            start_angle, end_angle = angle, 360 - angle
        elif self.direction == 'LEFT':
            start_angle, end_angle = 180 + angle, 180 - angle
        elif self.direction == 'UP':
            start_angle, end_angle = 90 + angle, 90 - angle
        else:
            start_angle, end_angle = 270 + angle, 270 - angle

        center = (self.radius, self.radius)
        points = [center]
        steps = 30

        for i in range(steps + 1):
            if start_angle < end_angle:
                current_angle = start_angle + (end_angle - start_angle) * i / steps
            else:
                current_angle = start_angle + (360 - start_angle + end_angle) * i / steps
                if current_angle > 360:
                    current_angle -= 360
            rad = math.radians(current_angle)
            x = center[0] + self.radius * math.cos(rad)
            y = center[1] - self.radius * math.sin(rad)
            points.append((x, y))

        pygame.draw.polygon(self.image, YELLOW, points)

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


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = 8
        self.direction = direction

    def update(self):
        self.rect.x += self.direction.x * self.velocity
        self.rect.y += self.direction.y * self.velocity
        if self.rect.right < 0 or self.rect.left > 606 or self.rect.bottom < 0 or self.rect.top > 606:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((255, 0, 0))  # rojo
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.direction = direction

    def update(self):
        dx = self.speed * (1 if self.direction == "RIGHT" else -1 if self.direction == "LEFT" else 0)
        dy = self.speed * (1 if self.direction == "DOWN" else -1 if self.direction == "UP" else 0)

        self.rect.x += dx
        self.rect.y += dy

        # Eliminar si sale de pantalla
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
