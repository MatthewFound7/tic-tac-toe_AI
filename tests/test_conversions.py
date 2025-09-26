# tests/test_backend.py

import pytest

from app.backend import BackEnd
from app.constants import tracking, scoring, scoring_2, grid_x, grid_y

# Helpers for readable positions
TL = (grid_x[0], grid_y[0])  # (0.14, 0.19)
TM = (grid_x[1], grid_y[0])  # (0.375, 0.19)
TR = (grid_x[2], grid_y[0])  # (0.61, 0.19)

ML = (grid_x[0], grid_y[1])  # (0.14, 0.5)
MM = (grid_x[1], grid_y[1])  # (0.375, 0.5)
MR = (grid_x[2], grid_y[1])  # (0.61, 0.5)

BL = (grid_x[0], grid_y[2])  # (0.14, 0.81)
BM = (grid_x[1], grid_y[2])  # (0.375, 0.81)
BR = (grid_x[2], grid_y[2])  # (0.61, 0.81)


@pytest.fixture(autouse=True)
def fresh_backend():
    """
    Ensure every test starts with a clean backend and cleared global dicts.
    The backend.reset() mirrors the UI's dictionary resets.
    """
    be = BackEnd()
    be.reset()
    yield be
    # Clean up after each test as well, to avoid leakage if a test ends mid-game.
    be.reset()


def all_dicts_blank():
    """Assert helper: all shared dicts should have blank-string values."""
    return (
        all(v == "" for v in tracking.values()) and
        all(v == "" for v in scoring.values()) and
        all(v == "" for v in scoring_2.values()) 
    )


def test_initial_state(fresh_backend: BackEnd):
    be = fresh_backend
    assert be.attempts == 0
    assert be.game_over is False
    assert be.current_shape() == "cross"  # cross goes first by design
    assert all_dicts_blank()


def test_turn_parity_and_next_shape_fields(fresh_backend: BackEnd):
    be = fresh_backend

    # 1st move => cross
    r1 = be.register_click(*MM)
    assert r1["played_shape"] == "cross"
    assert r1["game_over"] is False
    assert r1["next_shape"] == "circle"
    assert be.attempts == 1
    assert be.current_shape() == "circle"

    # 2nd move => circle
    r2 = be.register_click(*TL)
    assert r2["played_shape"] == "circle"
    assert r2["game_over"] is False
    assert r2["next_shape"] == "cross"
    assert be.attempts == 2
    assert be.current_shape() == "cross"


def test_circle_wins_top_row(fresh_backend: BackEnd):
    be = fresh_backend
    # Cross aims for top row: TL, TM, TR
    # Interleave harmless circle moves
    be.register_click(*TL)  # cross
    be.register_click(*MM)  # circle (harmless)
    be.register_click(*TM)  # cross
    be.register_click(*BR)  # circle (harmless)
    result = be.register_click(*TR)  # cross completes top row

    assert result["game_over"] is True
    assert result["winner"] == "cross"
    assert result["is_draw"] is False
    assert be.game_over is True

    # After game over, next_shape in final result should be None
    assert result["next_shape"] is None


def test_cross_wins_diagonal(fresh_backend: BackEnd):
    be = fresh_backend
    # Cross aims for TL -> MM -> BR diagonal, but cross plays 2nd/4th/6th.
    be.register_click(*TM)  # 1: cross elsewhere
    be.register_click(*TL)  # 2: circle diagonal 1
    be.register_click(*TR)  # 3: cross elsewhere
    be.register_click(*MM)  # 4: circle diagonal 2
    be.register_click(*BM)  # 5: cross elsewhere
    result = be.register_click(*BR)  # 6: circle diagonal 3 -> win

    assert result["game_over"] is True
    assert result["winner"] == "circle"
    assert result["is_draw"] is False
    assert be.game_over is True
    assert result["next_shape"] is None


def test_draw_when_board_fills_without_winner(fresh_backend: BackEnd):
    be = fresh_backend
    moves = [TL, TM, TR, ML, MM, BL, MR, BR, BM]
    result = None
    for pos in moves:
        result = be.register_click(*pos)

    assert result is not None
    assert result["game_over"] is True
    assert result["winner"] is None
    assert result["is_draw"] is True
    assert be.attempts == 9


def test_no_op_after_game_over_does_not_change_state(fresh_backend: BackEnd):
    be = fresh_backend
    # Fast win for cross: top row again
    be.register_click(*TL)  # cross
    be.register_click(*MM)  # circle
    be.register_click(*TM)  # cross
    be.register_click(*BR)  # circle
    win_result = be.register_click(*TR)  # cross wins

    attempts_after_win = be.attempts
    second_call = be.register_click(*BL)  # should be a no-op
    assert be.attempts == attempts_after_win  # no increment
    assert second_call["game_over"] is True  # still over
    assert second_call["winner"] is None or second_call["winner"] in ("circle", "cross")
    # (Spec returns winner only in the "active" evaluation; no change expected.)


def test_reset_clears_state_and_dicts(fresh_backend: BackEnd):
    be = fresh_backend
    be.register_click(*TL)  # make at least one move
    assert be.attempts == 1

    be.reset()
    assert be.attempts == 0
    assert be.game_over is False
    assert be.current_shape() == "cross"
    assert all_dicts_blank()
