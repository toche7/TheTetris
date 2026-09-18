import pygame

from .constants import (
    BACKGROUND,
    BOARD_X,
    BOARD_Y,
    CELL_SIZE,
    COLORS,
    GRID,
    MUTED_TEXT,
    PREVIEW_X,
    TEXT,
)
from .game import ActivePiece, TetrisGame


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.title_font = pygame.font.Font(None, 42)
        self.body_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def draw(self, game: TetrisGame) -> None:
        self.screen.fill(BACKGROUND)
        self._draw_board(game)
        self._draw_panel(game)
        if game.state == "paused":
            self._draw_overlay("PAUSED", "Press P to continue")
        elif game.state == "game_over":
            self._draw_overlay("GAME OVER", "Press R to restart")

    def _draw_board(self, game: TetrisGame) -> None:
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, 10 * CELL_SIZE, 20 * CELL_SIZE)
        pygame.draw.rect(self.screen, (25, 30, 41), board_rect)
        for row, cells in enumerate(game.board):
            for column, kind in enumerate(cells):
                if kind:
                    self._draw_cell(column, row, COLORS[kind])
                else:
                    pygame.draw.rect(
                        self.screen,
                        GRID,
                        (BOARD_X + column * CELL_SIZE, BOARD_Y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                        1,
                    )

        ghost = game.ghost_piece()
        if ghost:
            self._draw_piece(ghost, ghost=True)
        if game.active:
            self._draw_piece(game.active)

    def _draw_piece(self, piece: ActivePiece, ghost: bool = False) -> None:
        color = COLORS[piece.kind]
        for x, y in ((piece.x + dx, piece.y + dy) for dx, dy in self._shape_cells(piece)):
            if y >= 0:
                if ghost:
                    pygame.draw.rect(
                        self.screen,
                        color,
                        (BOARD_X + x * CELL_SIZE + 4, BOARD_Y + y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8),
                        2,
                    )
                else:
                    self._draw_cell(x, y, color)

    @staticmethod
    def _shape_cells(piece: ActivePiece):
        from .pieces import rotations

        states = rotations(piece.kind)
        return states[piece.rotation % len(states)]

    def _draw_cell(self, x: int, y: int, color) -> None:
        rect = pygame.Rect(BOARD_X + x * CELL_SIZE + 1, BOARD_Y + y * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect, border_radius=3)
        pygame.draw.line(self.screen, tuple(min(255, value + 35) for value in color), rect.topleft, rect.topright, 2)

    def _draw_panel(self, game: TetrisGame) -> None:
        self.screen.blit(self.title_font.render("TETRIS", True, TEXT), (PREVIEW_X, BOARD_Y))
        self.screen.blit(self.body_font.render("NEXT", True, MUTED_TEXT), (PREVIEW_X, BOARD_Y + 62))
        self._draw_preview(game.next_kind)
        info_y = BOARD_Y + 190
        for label, value in (("SCORE", game.score), ("LINES", game.lines), ("LEVEL", game.level)):
            self.screen.blit(self.small_font.render(label, True, MUTED_TEXT), (PREVIEW_X, info_y))
            self.screen.blit(self.body_font.render(str(value), True, TEXT), (PREVIEW_X, info_y + 22))
            info_y += 65
        self.screen.blit(self.small_font.render("Arrows: move / rotate", True, MUTED_TEXT), (PREVIEW_X, info_y + 10))
        self.screen.blit(self.small_font.render("Space: hard drop", True, MUTED_TEXT), (PREVIEW_X, info_y + 34))
        self.screen.blit(self.small_font.render("P: pause   R: restart", True, MUTED_TEXT), (PREVIEW_X, info_y + 58))

    def _draw_preview(self, kind: str) -> None:
        from .pieces import rotations

        for x, y in rotations(kind)[0]:
            pygame.draw.rect(
                self.screen,
                COLORS[kind],
                (PREVIEW_X + x * CELL_SIZE + 10, BOARD_Y + 100 + y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2),
                border_radius=3,
            )

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))
        title_surface = self.title_font.render(title, True, TEXT)
        subtitle_surface = self.body_font.render(subtitle, True, TEXT)
        center_x = self.screen.get_width() // 2
        self.screen.blit(title_surface, title_surface.get_rect(center=(center_x, 280)))
        self.screen.blit(subtitle_surface, subtitle_surface.get_rect(center=(center_x, 325)))
