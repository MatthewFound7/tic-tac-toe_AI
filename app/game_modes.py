# app/backend.py

import random
import pickle
from collections import defaultdict
from app.backend import BackEnd
from app.constants import *

# Inheriting from Backend: addition for easy game mode
class EasyMode(BackEnd):
    """
    Inherits from Backend but runs for a game against the computer in easy mode (random guessing)
    """
    def __init__(self):
        super().__init__()

    def data_logic(self, shape, x, y):
        """
        Casts to strings and updates `tracking`.
        """
        # run this to help comp track game state (knows where it can place a O)
        if self.attempts % 2 != 0:
            pos = self.easy_mode()
        else:
            x = str(x)
            y = str(y)
            pos = f"{x}, {y}"

        tracking[pos] = shape
        return pos

    # --- Convenience helpers used by the UI --
    def current_shape(self):
        """Who plays now (based on count parity)? 'X' (odd) or 'O' (even)."""
        return "O" if self.attempts % 2 != 0 else "X"

    def comp_move(self):
        """
        Handles whos turn it is for computer
        """
        return True if self.attempts % 2 != 0 else False
         
    def easy_mode(self):
        """
        Keeps track of available cells for computer
        """
        for k, v in tracking.items():
            if v != "":         
                comp_ads[k] = "used"
        available = [k for k in comp_ads if comp_ads[k] == "" and tracking[k] == ""]
        if available:
            return random.choice(available)
        else:
            raise ValueError("No available coordinates left!")  # for safety

# CURRENT INTERFACING OF AI LOGIC ONTO BACKEND
CELLS = [
    in0, in1, in2,
    in3, in4, in5,
    in6, in7, in8,
]

# Helpers for AI model to game interfacing
def board_state_from_tracking(tracking_dict, CELLS):
    """
    Keeps track of the game state as a string for computer reading
    """
    chars = []
    for pos in CELLS:
        v = tracking_dict.get(pos, "")
        chars.append('X' if v == "X" else 'O' if v == "O" else ' ')
    return ''.join(chars)

def legal_action_indices(tracking_dict):
    """Return list of indices (0..8) that are empty according to CELLS order."""
    return [i for i, pos in enumerate(CELLS) if tracking_dict.get(pos, "") == ""]

# Inheriting from backend: addition for ai powered game modes
class AIMode(BackEnd):
    def __init__(self, q_path=""):
        """
        Load the selected trained model and then wrap as a defaultdict(float) so missing pairs default to 0.0
        """
        super().__init__()
        with open(q_path, "rb") as f:
            loaded_Q = pickle.load(f)   
        self.Q = defaultdict(float, loaded_Q)

    def data_logic(self, shape, x, y):
        """
        Casts to strings and updates `tracking`.
        """
        # run this to help comp track game state (knows where it can place a O)
        if self.attempts % 2 != 0:
            pos = self.ih_mode()
        else:
            x = str(x)
            y = str(y)
            pos = f"{x}, {y}"

        tracking[pos] = shape
        return pos

    # --- Convenience helpers used by the UI ---
    def comp_move(self):
        """
        Tracks whos turn it is for computer
        """
        return True if self.attempts % 2 != 0 else False
        
    def ih_mode(self):
        """
        Keeps track of available cells for computer
        """
        # mark used cells in comp_ads like before
        for k, v in tracking.items():
            if v != "":
                comp_ads[k] = "used"

        available = [k for k in comp_ads if comp_ads[k] == "" and tracking[k] == ""]

        # --- Greedy Q choice ---
        ai_pos = self._greedy_q_move()

        # If, for any reason, the chosen cell isn't in `available` (e.g., mapping mismatch),
        # fall back to a random legal position so the game continues.
        if ai_pos in available:
            return ai_pos
        
    def _greedy_q_move(self):
        """
        Choose the argmax-Q action for the current board (constructed from `tracking`),
        breaking ties uniformly at random. Returns the UI position key (e.g. "x0,y0").
        Works by:
        - Building a string representation of the current board state (interfaces model onto game)
        - Finding all legal cells
        - looking up matching Q-values, and so can select the best play
        """
        state_strs = board_state_from_tracking(tracking, CELLS)
        legal_idxs = legal_action_indices(tracking)

        qvals = [(idx, self.Q[(state_strs, idx)]) for idx in legal_idxs]
        max_q = max(q for _, q in qvals)
        best_idxs = [idx for idx, q in qvals if q == max_q]
        idx = random.choice(best_idxs)  

        pos = CELLS[idx]

        return pos

