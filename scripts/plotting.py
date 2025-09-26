# app/ai/plotting.py
import matplotlib.pyplot as plt

def q_plotter(x_vals, y_vals):
    plt.plot(x_vals, y_vals, linestyle='-', label="Tic-Tac-Toe")
    plt.xlabel("Number of Episodes")
    plt.ylabel("Average Reward (rolling window)")
    plt.title("Tic-Tac-Toe Q-learning")
    plt.grid(True)
    plt.legend()
    plt.show()
