class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' '] * 9
        self.current = 'X'     
        self.done = False
        self.winner = None
        return self.state()

    def state(self):
        return ''.join(self.board)  

    def legal_actions(self):
        return [i for i, c in enumerate(self.board) if c == ' ']

    def step(self, action):
        """
        Apply 'action' for the current player, return (next_state, reward_for_X, done)
        """
        # Shouldn't ever run a step if action is not on the board, or the game is finished or the action is not an empty option (SAFETY)
        if self.done or action not in range(9) or self.board[action] != ' ':
            raise ValueError("Invalid action")

        # Finds the index of the action and changes it to the current move (at the start this is O the random)
        self.board[action] = self.current
        # Extracts winner player if check_winner not empty
        self.winner = self._check_winner()
        # If there is a winner, done is true, game is finished
        if self.winner or ' ' not in self.board:
            self.done = True

        # Reward is always from X's perspective
        reward = 0.0
        if self.done:
            if self.winner == 'O':
                reward = +1.0
            elif self.winner == 'X':
                reward = -1.0
            else:
                reward = 0.0

        if not self.done:
            self.current = 'X' if self.current == 'O' else 'O'

        return self.state(), reward, self.done

    def _check_winner(self):
        b = self.board
        lines = [
            (0,1,2),(3,4,5),(6,7,8),  # rows
            (0,3,6),(1,4,7),(2,5,8),  # cols
            (0,4,8),(2,4,6)           # diags
        ]
        for i, j, k in lines:
            if b[i] != ' ' and b[i] == b[j] == b[k]:
                return b[i]
        return None

    def render(self):
        b = self.board
        def cell(i):
            return b[i] if b[i] != ' ' else str(i)
        print(f"{cell(0)} | {cell(1)} | {cell(2)}")
        print("--+---+--")
        print(f"{cell(3)} | {cell(4)} | {cell(5)}")
        print("--+---+--")
        print(f"{cell(6)} | {cell(7)} | {cell(8)}")