
import numpy as np

# Define the environment
env = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Define the Q-table
q_table = np.zeros((env.shape[0], env.shape[1], 4))

# Define the hyperparameters
alpha = 0.1
gamma = 0.99
epsilon = 0.1
num_episodes = 1000

# Define the action space
actions = ['up', 'down', 'left', 'right']

# Define the helper function to choose an action


def choose_action(state):
    if np.random.uniform() < epsilon:
        # Choose a random action
        action = np.random.choice(actions)
    else:
        # Choose the action with the highest Q-value
        action = actions[np.argmax(q_table[state[0], state[1]])]
    return action

# Define the helper function to update the Q-table


def update_q_table(state, action, reward, next_state):
    q_table[state[0], state[1], actions.index(action)] += alpha * (reward + gamma * np.max(
        q_table[next_state[0], next_state[1]]) - q_table[state[0], state[1], actions.index(action)])


# Define the main Q-learning algorithm
for episode in range(num_episodes):
    # Reset the environment
    state = [0, 0]
    done = False
    while not done:
        # Choose an action
        action = choose_action(state)
        # Take the action
        if action == 'up':
            next_state = [max(state[0] - 1, 0), state[1]]
        elif action == 'down':
            next_state = [min(state[0] + 1, env.shape[0] - 1), state[1]]
        elif action == 'left':
            next_state = [state[0], max(state[1] - 1, 0)]
        elif action == 'right':
            next_state = [state[0], min(state[1] + 1, env.shape[1] - 1)]
        # Update the Q-table
        update_q_table(
            state, action, env[next_state[0], next_state[1]], next_state)
        # Update the state
        state = next_state
        # Check if the episode is done
        if state == [env.shape[0] - 1, env.shape[1] - 1]:
            done = True
    # Print the episode number
    print('Episode:', episode)
