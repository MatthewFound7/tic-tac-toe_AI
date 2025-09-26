# app/backend.py

from app.constants import *

class BackEnd:
    """
    Owns all game state + rules. The UI should only:
      - ask who the current/next player is (for icons/arrow),
      - register a click (x,y),
      - respond to the result (win/draw/continue),
      - call reset() when replaying.
      - and any other directly UI related tasks
    """

    def __init__(self):
        self.attempts = 0     
        self.game_over = False

    def data_logic(self, shape, x, y):
        """
        Casts to strings and updates `tracking`.
        """
        x = str(x)
        y = str(y)
        pos = f"{x}, {y}"
        tracking[pos] = shape
        return pos

    def current_shape(self):
        """Who plays now (based on count parity)? 'cross' (odd) or 'circle' (even)."""
        return "O" if self.attempts % 2 != 0 else "X"

    def next_shape(self):
        """Who plays after the current move?"""
        return "O" if self.current_shape() == "X" else "X"
    
    def selection_off(self):
        """Swith off game mode selection if game has started """
        if self.attempts >= 1:
            return True
        else:
            return False

    def register_click(self, x, y):
        """
        One-stop call for UI: record the move + run game logic + advance turn.
        Returns a dict the UI can use to decide what to render.
        """
        
        if self.game_over:
            # no-op if game already finished
            return {
                "game_over": True,
                "winner": None,
                "is_draw": False,
                "win_state": result,
                "played_shape": None,
                "next_shape": None,
                "attempts": self.attempts,
                "placed_at": None
            }

        played_shape = self.current_shape()  # decide who plays now
        
        # Update your original tracking structure
        placed_pos = self.data_logic(played_shape, x, y)

        # After a successful placement, advance counter
        self.attempts += 1
        
        # Run the same win/draw logic you had in the UI
        result = self._evaluate_game_state()
        
        # If not over, compute the next player for the arrow
        result.update({
            "played_shape": played_shape,
            "next_shape": None if result["game_over"] else self.current_shape(),
            "attempts": self.attempts,
            "placed_at": placed_pos
        })
        
        return result

    def _evaluate_game_state(self):
        """
        Fills dictionaries which are then compared against all possible win conditions
        """

        # ---- cross checking (fills `scoring`) ----
        for pos, shape in tracking.items():
            if shape == "X":
                scoring[pos] = "hit"
            else:
                scoring[pos] = "miss"

        # Compare with each win condition
        for i in range(len(win_conditions)):
            vals1 = list(scoring.values())
            vals2 = list(win_conditions[i].values())

            results = []
            for k in range(len(scoring)):
                results.append(vals1[k] == vals2[k] == "hit")

            if sum(results) == 3:
                self.game_over = True
                return {
                    "game_over": True,
                    "winner": "X",
                    "is_draw": False,
                    "win_state": results
                }

        # ---- circle checking (fills `scoring_2`) ----
        for j, item in tracking.items():
            if item == "O":
                scoring_2[j] = "hit"
            else:
                scoring_2[j] = "miss"

        for k in range(len(win_conditions)):
            vals3 = list(scoring_2.values())
            vals4 = list(win_conditions[k].values())

            answers = []
            for n in range(len(scoring_2)):
                answers.append(vals3[n] == vals4[n] == "hit")

            if sum(answers) == 3:
                self.game_over = True
                return {
                    "game_over": True,
                    "winner": "O",
                    "is_draw": False,
                    "win_state": answers
                }

        # ---- draw? ----
        if self.attempts == 9 and not self.game_over:
            self.game_over = True
            return {
                "game_over": True,
                "winner": None,
                "is_draw": True,
                "win_state": None
            }

        # ---- otherwise game continues ----
        return {"game_over": False, "winner": None, "is_draw": False, "win_state": None}
        
    def reset(self):
        """
        Dictionary resets and counters.
        The UI should call this, then only clear its widgets.
        """

        self.attempts = 0
        self.game_over = False

        # Reset the original dicts (same keys, blank values)
        for i in scoring:
            scoring[i] = ""
        for i in tracking:
            tracking[i] = ""
        for i in scoring_2:
            scoring_2[i] = ""
        for i in comp_ads:
            comp_ads[i] = ""
    
   