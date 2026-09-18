import pygame

from .constants import BACKGROUND, WINDOW_HEIGHT, WINDOW_WIDTH
from .game import TetrisGame
from .music import MusicPlayer
from .renderer import Renderer


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = TetrisGame()
    renderer = Renderer(screen)
    music = MusicPlayer()
    music.start()
    running = True

    while running:
        elapsed = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p and game.state != "game_over":
                    game.state = "paused" if game.state == "playing" else "playing"
                elif event.key == pygame.K_r:
                    game.reset()
                elif game.state == "playing":
                    if event.key == pygame.K_LEFT:
                        game.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1)
                    elif event.key == pygame.K_DOWN:
                        game.hard_drop()
                    elif event.key == pygame.K_UP:
                        game.rotate()
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()

        game.tick(elapsed)
        renderer.draw(game)
        pygame.display.flip()

    music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
