from constants import *
from entities import *
from maze import *
import os

def load_ghost_images():
    ghost_images = {}
    try:
        path = os.path.join("assets", "images")

        ghost_images['red'] = pygame.image.load(os.path.join(path, "rojo.png")).convert_alpha()
        ghost_images['pink'] = pygame.image.load(os.path.join(path, "rosa.png")).convert_alpha()
        ghost_images['orange'] = pygame.image.load(os.path.join(path, "naranja.png")).convert_alpha()
        ghost_images['cyan'] = pygame.image.load(os.path.join(path, "celeste.png")).convert_alpha()  # nuevo fantasma

        for color in ghost_images:
            ghost_images[color] = pygame.transform.scale(ghost_images[color], (20, 20))

        # Fantasmas vulnerables (azul parpadeante)
        ghost_images['vulnerable'] = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(ghost_images['vulnerable'], VULNERABLE_COLOR, [0, 0, 20, 20])

        blink1 = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(blink1, WHITE, [0, 0, 20, 20])
        ghost_images['blink'] = [ghost_images['vulnerable'], blink1]

        return ghost_images
    except Exception as e:
        print("Error cargando imágenes de los fantasmas:", e)
        return None



class Game:
    def __init__(self, alias):
        self.player_can_shoot = False
        self.shoot_timer = 0
        self.projectiles = pygame.sprite.Group()
        self.sfx_channel = pygame.mixer.Channel(1)  # canal 1 para efectos
        self.paused = False
        self.alias = alias
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.gate = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.special_pellets = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.player = None
        self.initialize_game()

    def initialize_game(self):
        self.bullets = pygame.sprite.Group()
        self.pellets, self.special_pellets = setup_pellets(self.all_sprites, self.walls)
        self.play_music("pac-man-background-music.mp3")
        self.sfx_channel = pygame.mixer.Channel(1)
        self.chomp_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "pac-man-comiendo.wav"))
        self.chomp_sound.set_volume(0.4)
        self.all_sprites.empty()
        self.walls = setup_walls(self.all_sprites)
        self.gate = setup_gate(self.all_sprites)
        self.pellets, self.special_pellets = setup_pellets(self.all_sprites, self.walls)
        self.player = Player(300, 400)
        self.all_sprites.add(self.player)

        ghost_images = load_ghost_images()  # ← AQUI
        ghost_positions = [(150, 200), (300, 200), (450, 200), (225, 250)]
        ghost_colors = ['red', 'pink', 'orange','cyan']
        for color, pos in zip(ghost_colors, ghost_positions):
            ghost = Ghost(color, pos[0], pos[1], ghost_images)
            self.ghosts.add(ghost)
            self.all_sprites.add(ghost)

    def load_sound(self, filename, volume=1.0):
        try:
            path = os.path.join("assets", "sounds", filename)
            sound = pygame.mixer.Sound(path)
            sound.set_volume(volume)
            return sound
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el sonido '{filename}':", e)
            return None

    def play_music(self, filename, loop=True):
        try:
            path = os.path.join("assets", "sounds", filename)
            pygame.mixer.music.load(path)
            pygame.mixer.music.play(-1 if loop else 0)
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la música '{filename}':", e)


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self, 'pause_rect') and self.pause_rect.collidepoint(event.pos):
                    self.paused = True
                    pygame.mixer.music.pause()
                    self.sfx_channel.stop()

                # Si está pausado y hace clic en "Reanudar"
                if self.paused and hasattr(self, 'resume_button') and self.resume_button.collidepoint(event.pos):
                    self.paused = False
                    pygame.mixer.music.unpause()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.paused:
                continue

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.changespeed(-4, 0)
                elif event.key == pygame.K_SPACE and self.player_can_shoot:
                    self.fire_bullet()
                elif event.key == pygame.K_RIGHT:
                    self.player.changespeed(4, 0)
                elif event.key == pygame.K_UP:
                    self.player.changespeed(0, -4)
                elif event.key == pygame.K_DOWN:
                    self.player.changespeed(0, 4)

                # ✅ Disparo solo si tiene el poder activo
                elif event.key == pygame.K_SPACE and self.player_can_shoot:
                    direction = pygame.Vector2(0, 0)
                    if self.player.direction == 'RIGHT':
                        direction = pygame.Vector2(1, 0)
                    elif self.player.direction == 'LEFT':
                        direction = pygame.Vector2(-1, 0)
                    elif self.player.direction == 'UP':
                        direction = pygame.Vector2(0, -1)
                    elif self.player.direction == 'DOWN':
                        direction = pygame.Vector2(0, 1)

                    projectile = Projectile(self.player.rect.centerx, self.player.rect.centery, direction)
                    self.projectiles.add(projectile)
                    self.all_sprites.add(projectile)



            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.player.changespeed(0, self.player.change_y)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    self.player.changespeed(self.player.change_x, 0)

            elif self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self, 'resume_button') and self.resume_button.collidepoint(event.pos):
                    self.paused = False
                    pygame.mixer.music.unpause()


            elif event.type >= pygame.USEREVENT and event.type < pygame.USEREVENT + len(self.ghosts):
                ghost_index = event.type - pygame.USEREVENT
                ghost = list(self.ghosts)[ghost_index]
                ghost.respawn()

    def update(self):
        self.bullets.update()
        self.player.update(self.walls, self.gate)
        self.ghosts.update(self.walls, self.gate)
        self.check_collisions()
        # Reproducir sonido de movimiento solo si se está moviendo
        if not self.game_over and (self.player.change_x != 0 or self.player.change_y != 0):
            if not self.sfx_channel.get_busy():
                self.sfx_channel.play(self.chomp_sound, loops=-1)
        else:
            self.sfx_channel.stop()
        self.projectiles.update()
        # Verificar colisión proyectil vs fantasmas
        for projectile in self.projectiles:
            ghost_hit = pygame.sprite.spritecollideany(projectile, self.ghosts)
            if ghost_hit and ghost_hit.vulnerable and ghost_hit.active:
                ghost_hit.active = False
                self.score += 200
                pygame.time.set_timer(pygame.USEREVENT + list(self.ghosts).index(ghost_hit), 3000, True)
                projectile.kill()
        # Desactivar disparo después de 5 segundos
        if self.player_can_shoot and pygame.time.get_ticks() - self.shoot_timer > 5000:
            self.player_can_shoot = False

    def draw(self, screen):
        screen.fill(BLACK)
        self.all_sprites.draw(screen)
        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Puntaje: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            self.show_game_over_message(screen)

        # Dibuja botón de pausa (símbolo ||)
        pause_rect = pygame.Rect(278, 10, 50, 30)
        pygame.draw.rect(screen, WHITE, pause_rect, border_radius=5)
        pygame.draw.line(screen, BLACK, (pause_rect.x + 10, pause_rect.y + 5), (pause_rect.x + 10, pause_rect.y + 25),
                         4)
        pygame.draw.line(screen, BLACK, (pause_rect.x + 30, pause_rect.y + 5), (pause_rect.x + 30, pause_rect.y + 25),
                         4)
        self.pause_rect = pause_rect  # guardar para detectar clic

    def check_collisions(self):
        # Comer pastillas normales
        pellets_hit = pygame.sprite.spritecollide(self.player, self.pellets, True)
        if pellets_hit:
            self.score += 10 * len(pellets_hit)

        # Comer pastillas especiales
        special_hit = pygame.sprite.spritecollide(self.player, self.special_pellets, True)
        for pellet in special_hit:
            self.score += 50
            for ghost in self.ghosts:
                ghost.make_vulnerable()

            # Si el pellet era el de disparo (posición específica)
            if pellet.rect.center == (380, 220):
                self.player_can_shoot = True
                self.shoot_timer = pygame.time.get_ticks()
                print("🟠 Poder de disparo activado")

        # Colisión con fantasmas
        ghosts_hit = pygame.sprite.spritecollide(self.player, self.ghosts, False)
        for ghost in ghosts_hit:
            if ghost.vulnerable and ghost.active:
                ghost.active = False
                self.score += 200
                ghost_index = list(self.ghosts).index(ghost)
                pygame.time.set_timer(pygame.USEREVENT + list(self.ghosts).index(ghost), 3000, True)
            elif not ghost.vulnerable and ghost.active:
                self.lives -= 1
                self.game_over = True
                pygame.mixer.music.pause()
                self.sfx_channel.stop()

    def reset_level(self):
        self.initialize_game()

    def next_level(self):
        self.level += 1
        self.reset_level()
    def show_game_over_message(self, screen):
        font = pygame.font.SysFont("Comic Sans MS", 36)
        msg1 = font.render("DESDOLARIZADO por Luisa", True, WHITE)
        msg2 = font.render("ENTER = Jugar con el mismo alias", True, WHITE)
        msg3 = font.render("SPACE = Jugar con nuevo alias", True, WHITE)

        screen.blit(msg1, msg1.get_rect(center=(303, 240)))
        screen.blit(msg2, msg2.get_rect(center=(303, 290)))
        screen.blit(msg3, msg3.get_rect(center=(303, 340)))

    # Funcion para poner pausa a mitad de juego
    def draw_pause_menu(self, screen):
        width, height = 606, 606
        menu_width, menu_height = int(width * 0.6), int(height * 0.6)
        menu_x = (width - menu_width) // 2
        menu_y = (height - menu_height) // 2

        pause_menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, LIGHT_BLUE, pause_menu_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, pause_menu_rect, 2, border_radius=10)

        font = pygame.freetype.SysFont("Comic Sans MS", 32)
        font.render_to(screen, (pause_menu_rect.centerx - 50, pause_menu_rect.top + 30), "PAUSA", BLACK)

        # Botón reanudar centrado dentro del menú
        button_width, button_height = 150, 50
        button_x = pause_menu_rect.centerx - button_width // 2
        button_y = pause_menu_rect.centery
        self.resume_button = pygame.Rect(button_x, button_y, button_width, button_height)

        pygame.draw.rect(screen, (0, 200, 0), self.resume_button, border_radius=8)
        font.render_to(screen, (self.resume_button.x + 20, self.resume_button.y + 10), "Reanudar", WHITE)

    def draw_game_over_menu(self, screen):
        width, height = 606, 606
        menu_width, menu_height = int(width * 0.7), int(height * 0.7)
        menu_x = (width - menu_width) // 2
        menu_y = (height - menu_height) // 2

        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(screen, LIGHT_BLUE, menu_rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, menu_rect, 2, border_radius=12)

        font = pygame.freetype.SysFont("Comic Sans MS", 28)
        big_font = pygame.freetype.SysFont("Comic Sans MS", 34)

        big_font.render_to(screen, (menu_rect.x + 40, menu_rect.y + 40), "DESDOLARIZADO por Luisa", RED)
        font.render_to(screen, (menu_rect.x + 40, menu_rect.y + 120), "ENTER = Reintentar", BLACK)
        font.render_to(screen, (menu_rect.x + 40, menu_rect.y + 160), "SPACE = Nuevo alias", BLACK)

    def fire_bullet(self):
        bullet = Bullet(self.player.rect.centerx, self.player.rect.centery, self.player.direction)
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

