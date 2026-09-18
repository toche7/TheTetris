from dataclasses import dataclass
from typing import List, Optional, Tuple

from .constants import BOARD_HEIGHT, BOARD_WIDTH, DROP_INTERVALS, LINE_POINTS
from .pieces import Cell, SevenBag, rotations


@dataclass
class ActivePiece:
    kind: str
    x: int
    y: int
    rotation: int = 0


class TetrisGame:
    def __init__(self, seed: int = None) -> None:
        self.randomizer = SevenBag(seed)
        self.board: List[List[Optional[str]]] = []
        self.active: Optional[ActivePiece] = None
        self.next_kind = "I"
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = "playing"
        self.drop_timer = 0.0
        self.reset()

    def reset(self) -> None:
        self.board = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.state = "playing"
        self.drop_timer = 0.0
        self.next_kind = self.randomizer.next()
        self._spawn()

    @property
    def drop_interval(self) -> float:
        return DROP_INTERVALS[min(self.level - 1, len(DROP_INTERVALS) - 1)]

    def cells(self, piece: Optional[ActivePiece] = None) -> Tuple[Cell, ...]:
        piece = piece or self.active
        if piece is None:
            return ()
        shape = rotations(piece.kind)[piece.rotation % len(rotations(piece.kind))]
        return tuple((piece.x + x, piece.y + y) for x, y in shape)

    def can_place(self, piece: ActivePiece) -> bool:
        for x, y in self.cells(piece):
            if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT:
                return False
            if y >= 0 and self.board[y][x] is not None:
                return False
        return True

    def move(self, dx: int, dy: int = 0) -> bool:
        if self.state != "playing" or self.active is None:
            return False
        candidate = ActivePiece(self.active.kind, self.active.x + dx, self.active.y + dy, self.active.rotation)
        if self.can_place(candidate):
            self.active = candidate
            return True
        return False

    def rotate(self) -> bool:
        if self.state != "playing" or self.active is None:
            return False
        candidate = ActivePiece(self.active.kind, self.active.x, self.active.y, self.active.rotation + 1)
        for offset in (0, -1, 1, -2, 2):
            kicked = ActivePiece(candidate.kind, candidate.x + offset, candidate.y, candidate.rotation)
            if self.can_place(kicked):
                self.active = kicked
                return True
        return False

    def hard_drop(self) -> int:
        distance = 0
        while self.move(0, 1):
            distance += 1
        self.lock()
        self.score += distance * 2
        return distance

    def tick(self, elapsed: float) -> None:
        if self.state != "playing":
            return
        self.drop_timer += elapsed
        while self.drop_timer >= self.drop_interval:
            self.drop_timer -= self.drop_interval
            if not self.move(0, 1):
                self.lock()
                break

    def lock(self) -> None:
        if self.active is None:
            return
        for x, y in self.cells():
            if y < 0:
                self.state = "game_over"
                return
            self.board[y][x] = self.active.kind
        cleared = self._clear_lines()
        self.lines += cleared
        self.score += LINE_POINTS[cleared] * self.level
        self.level = self.lines // 10 + 1
        self._spawn()

    def ghost_piece(self) -> Optional[ActivePiece]:
        if self.active is None:
            return None
        ghost = ActivePiece(self.active.kind, self.active.x, self.active.y, self.active.rotation)
        while self.can_place(ActivePiece(ghost.kind, ghost.x, ghost.y + 1, ghost.rotation)):
            ghost.y += 1
        return ghost

    def _clear_lines(self) -> int:
        remaining = [row for row in self.board if any(cell is None for cell in row)]
        cleared = BOARD_HEIGHT - len(remaining)
        self.board = [[None] * BOARD_WIDTH for _ in range(cleared)] + remaining
        return cleared

    def _spawn(self) -> None:
        kind = self.next_kind
        self.next_kind = self.randomizer.next()
        shape = rotations(kind)[0]
        width = max(x for x, _ in shape) + 1
        self.active = ActivePiece(kind, (BOARD_WIDTH - width) // 2, -1)
        if not self.can_place(self.active):
            self.state = "game_over"
