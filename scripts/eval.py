import random

def play_greedy_episode(env, agent, verbose=False):
    s = env.reset()
    done = False
    steps = 0
    if verbose:
        print("\nGreedy episode (X=agent):")
        env.render()
    while not done and steps < 9:
        if env.current == 'O':
            a = agent.greedy_action(s, env.legal_actions())
            s, r, done = env.step(a)
            if verbose:
                print("\nO plays", a)
                env.render()
        else:
            oa = random.choice(env.legal_actions())
            s, r, done = env.step(oa)
            if verbose:
                print("\nX plays", oa)
                env.render()
        steps += 1
    return r  

def human_vs_agent(env, agent):
    """
    Human plays O and moves first.
    Agent remains X and always plays greedily.
    """
    print("\nYou are X and MOVE FIRST. Indices 0..8.")
    s = env.reset()

    # ----- Human's opening move -----
    env.render()
    legal = env.legal_actions()
    move = None
    while move not in legal:
        try:
            move = int(input(f"Your first move (choose from {legal}): "))
        except Exception:
            move = None
    s, r, done = env.step(move)  
    print("\nYou played", move)
    env.render()
    if done:
        print("\nResult:", "You (X) win!" if env.winner == 'X' else "Draw")
        return

    # ----- Alternating turns -----
    while True:
        a = agent.greedy_action(s, env.legal_actions())
        s, r, done = env.step(a)
        print("\nO plays", a)
        env.render()
        if done:
            print("\nResult:", "O wins!" if env.winner == 'O' else "Draw")
            break

        legal = env.legal_actions()
        move = None
        while move not in legal:
            try:
                move = int(input(f"Your move (choose from {legal}): "))
            except Exception:
                move = None
        s, r, done = env.step(move)
        print("\nYou played", move)
        env.render()
        if done:
            print("\nResult:", "You (X) win!" if env.winner == 'X' else "Draw")
            break