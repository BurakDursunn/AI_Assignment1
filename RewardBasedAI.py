import random
import time


class RewardBasedAI:
    def __init__(self, learning_rate=0.1, exploration_prob=0.1, discount_factor=0.9):
        """
        Constructor for RewardBasedAI class.

        Parameters:
        - learning_rate (float): Learning rate for updating Q values.
        - exploration_prob (float): Probability of exploration in epsilon-greedy strategy.
        - discount_factor (float): Discount factor for updating Q values.
        """
        self.learning_rate = learning_rate
        self.exploration_prob = exploration_prob
        self.discount_factor = discount_factor
        self.q_values = {}

    def decide_action(self, current_state):
        """
        Choose an action based on epsilon-greedy strategy.

        Parameters:
        - current_state (str): Current state of the environment.

        Returns:
        - Selected action (str).
        """
        random.seed(time.time())
        if random.random() < self.exploration_prob:
            # If current room is A, only go right, if current room is B, go left or right, if current room is C, only go left
            actions = ['suck', 'no-op']
            if current_state == "A":
                actions.append('right')
            elif current_state == "B":
                actions.append('left')
                actions.append('right')
            elif current_state == "C":
                actions.append('left')

            # Explore: Choose a random action
            return random.choice(actions)
        else:
            # Exploit: Choose the action with the highest Q value
            # If current room is A, only go right, if current room is B, go left or right, if current room is C, only go left
            possible_actions = ['suck', 'no-op']
            if current_state == "A":
                possible_actions.append('right')
                selected_action = max(possible_actions,
                                      key=lambda action: self.q_values.get(current_state, {'suck': 0, 'no-op': 0, 'right': 0}).get(action, 0))
            elif current_state == "B":
                possible_actions.extend(['left', 'right'])
                selected_action = max(possible_actions,
                                      key=lambda action: self.q_values.get(current_state, {'suck': 0, 'no-op': 0, 'left': 0, 'right': 0}).get(action, 0))
            elif current_state == "C":
                possible_actions.append('left')
                selected_action = max(possible_actions,
                                      key=lambda action: self.q_values.get(current_state, {'suck': 0, 'no-op': 0, 'left': 0}).get(action, 0))

            return selected_action

    def update_q_values(self, current_state, action, reward, next_state):
        """
        Update Q values based on the Bellman equation.

        Parameters:
        - current_state (str): Current state of the environment.
        - action (str): Selected action.
        - reward (float): Reward obtained from the action.
        - next_state (str): Next state of the environment.
        """
        current_q_value = self.q_values.get(
            current_state, {'suck': 0, 'no-op': 0, 'left': 0, 'right': 0})[action]
        max_next_q_value = max(self.q_values.get(
            next_state, {'suck': 0, 'no-op': 0, 'left': 0, 'right': 0}).values())

        # Discounted future reward
        discounted_future_reward = self.discount_factor * max_next_q_value

        new_q_value = current_q_value + self.learning_rate * \
            (reward + discounted_future_reward - current_q_value)

        if current_state not in self.q_values:
            self.q_values[current_state] = {
                'suck': 0, 'no-op': 0, 'left': 0, 'right': 0}

        self.q_values[current_state][action] = new_q_value
