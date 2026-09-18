from tetris.game import ActivePiece, TetrisGame


def test_piece_moves_and_stops_at_floor():
    game = TetrisGame(seed=1)
    while game.move(0, 1):
        pass
    y = game.active.y
    assert not game.move(0, 1)
    assert game.active.y == y


def test_hard_drop_locks_piece_and_scores():
    game = TetrisGame(seed=1)
    distance = game.hard_drop()
    assert distance > 0
    assert game.score >= distance * 2
    assert any(cell is not None for row in game.board for cell in row)


def test_full_line_is_cleared():
    game = TetrisGame(seed=1)
    game.board[-1] = ["I"] * 10
    game.active = ActivePiece("O", 3, 17)
    game.lock()
    assert game.lines == 1
    assert all(cell is None for cell in game.board[0])


def test_rotation_does_not_leave_board():
    game = TetrisGame(seed=1)
    game.active = ActivePiece("I", 0, 0)
    assert game.rotate()
    assert all(0 <= x < 10 and 0 <= y < 20 for x, y in game.cells())


def test_game_over_when_spawn_is_blocked():
    game = TetrisGame(seed=1)
    game.board[0][4] = "I"
    game.board[0][5] = "I"
    game.active = ActivePiece("O", 4, 0)
    game.lock()
    assert game.state == "game_over"
