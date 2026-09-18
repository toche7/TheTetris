import random
from typing import Dict, List, Sequence, Tuple

Cell = Tuple[int, int]
PieceShape = Tuple[Cell, ...]

BASE_SHAPES: Dict[str, PieceShape] = {
    "I": ((0, 1), (1, 1), (2, 1), (3, 1)),
    "J": ((0, 0), (0, 1), (1, 1), (2, 1)),
    "L": ((2, 0), (0, 1), (1, 1), (2, 1)),
    "O": ((1, 0), (2, 0), (1, 1), (2, 1)),
    "S": ((1, 0), (2, 0), (0, 1), (1, 1)),
    "T": ((1, 0), (0, 1), (1, 1), (2, 1)),
    "Z": ((0, 0), (1, 0), (1, 1), (2, 1)),
}


def _rotate(shape: Sequence[Cell]) -> PieceShape:
    rotated = [(y, -x) for x, y in shape]
    min_x = min(x for x, _ in rotated)
    min_y = min(y for _, y in rotated)
    return tuple(sorted((x - min_x, y - min_y) for x, y in rotated))


def rotations(kind: str) -> Tuple[PieceShape, ...]:
    states: List[PieceShape] = []
    shape = BASE_SHAPES[kind]
    for _ in range(4):
        if shape not in states:
            states.append(shape)
        shape = _rotate(shape)
    return tuple(states)


class SevenBag:
    def __init__(self, seed: int = None) -> None:
        self._random = random.Random(seed)
        self._queue: List[str] = []

    def next(self) -> str:
        if not self._queue:
            self._queue.extend(BASE_SHAPES)
            self._random.shuffle(self._queue)
        return self._queue.pop(0)
