import random
from collections import defaultdict

class QAgent:
    def __init__(self, epsilon=0.0, alpha=0.0, gamma=0.0):
        self.Q = defaultdict(float)  
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def select_action(self, state, legal_actions):
        if not legal_actions:
            return None
        if random.random() < self.epsilon:
            return random.choice(legal_actions)
        qvals = [self.Q[(state, a)] for a in legal_actions]
        maxq = max(qvals)
        best = [a for a, q in zip(legal_actions, qvals) if q == maxq]
        return random.choice(best)

    def greedy_action(self, state, legal_actions):
        if not legal_actions:
            return None
        qvals = [self.Q[(state, a)] for a in legal_actions]
        maxq = max(qvals)
        best = [a for a, q in zip(legal_actions, qvals) if q == maxq]
        return random.choice(best)

    def update(self, s, a, r, s_next, legal_next, done):
        if done or not legal_next:
            target = r
        else:
            max_next = max(self.Q[(s_next, an)] for an in legal_next)
            target = r + self.gamma * max_next
        self.Q[(s, a)] += self.alpha * (target - self.Q[(s, a)])