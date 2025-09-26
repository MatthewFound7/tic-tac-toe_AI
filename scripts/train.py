import random
from .agent import QAgent

def play_one_training_episode(env, agent, opponent='random', max_plies=9):
    """
    One full game where X (agent) and O (opponent) alternate moves.
    Returns total reward for X in the episode.
    """
    # always start each episode with a fresh game board and reward management
    s = env.reset()
    total_r = 0.0

    for _ in range(max_plies):
        if env.current == 'O':
            a = agent.select_action(s, env.legal_actions())
            s_next, r, done = env.step(a)
            total_r += r

            # if game finished
            if done:
                agent.update(s, a, r, s_next, [], True)
                break

            # Opponent immediate move (random by default)
            oa = random.choice(env.legal_actions()) if opponent == 'random' else random.choice(env.legal_actions())
            s_mid, r_mid, done_mid = env.step(oa)

            if done_mid:
                agent.update(s, a, r_mid, s_mid, [], True)
                total_r += r_mid
                break
            else:
                # Non-terminal transition
                agent.update(s, a, 0.0, s_mid, env.legal_actions(), False)
                s = s_mid
        else:
            # (Shouldn't happen since X always starts, but keep robust)
            oa = random.choice(env.legal_actions())
            s, r, done = env.step(oa)
            if done:
                break
                
    return total_r

def q_learning(
    env,
    episodes=500,
    alpha=0.1,
    gamma=0.95,
    epsilon=0.2,
    epsilon_min=0.01,
    epsilon_decay=0.995,
    log_slices=20,
    avg_window_frac=0.2
):
    agent = QAgent(epsilon=epsilon, alpha=alpha, gamma=gamma)
    rewards = []
    window = max(5, int(episodes * avg_window_frac))

    x_vals, y_vals = [], []

    for ep in range(1, episodes + 1):
        # Play one training episode
        total = play_one_training_episode(env, agent, opponent='random')
        rewards.append(total)

        # Decay epsilon
        agent.epsilon = max(epsilon_min, agent.epsilon * epsilon_decay)

        # Periodic logging + plotting points
        if ep % max(1, episodes // log_slices) == 0:
            avg = sum(rewards[-window:]) / len(rewards[-window:])
            print(f"Episode {ep:5d} | eps={agent.epsilon:.3f} | avg_reward({window})={avg:.3f}")
            x_vals.append(ep)
            y_vals.append(avg)

        # if ep % 20000 == 0:  # every 500 episodes
        #     # Show the start-state values for all 9 actions
        #     chosen_state = "    O    "
        #     start_vals = {a: round(agent.Q[(chosen_state, a)], 3) for a in range(9)}
        #     print(f"Episode {ep:5d} | Q(start) = {start_vals}")


    return agent, rewards