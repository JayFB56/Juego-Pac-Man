import pygame
from menu import Menu
from game import Game
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CAPTION

def main():
    pygame.mixer.init()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(CAPTION)
    clock = pygame.time.Clock()

    menu = Menu()
    game = None
    running = True

    while running:
        events = pygame.event.get()  # Procesa eventos solo una vez

        if game is None:
            # Menú activo
            menu.draw(screen)
            pygame.display.update()
            if menu.handle_events(events):
                game = Game(menu.alias)

        else:
            if game.game_over:
                # GAME OVER → esperar acción del jugador
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            game = Game(game.alias)
                            pygame.mixer.music.play(-1)

                        elif event.key == pygame.K_SPACE:
                            pygame.mixer.music.stop()
                            game = None  # volver al menú principal
                if game:
                    game.draw(screen)
                    game.draw_game_over_menu(screen)


            elif game.paused:
                # PAUSA ACTIVADA
                game.handle_events(events)
                game.draw(screen)
                game.draw_pause_menu(screen)

            else:
                # JUEGO ACTIVO
                game.handle_events(events)
                game.update()
                game.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()