import random


class QLearningAI:
    def __init__(self, actions):
        self.actions = actions
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = {}

    def get_q_value(self, current_room, action):
        return self.q_table.get((current_room, action), 0.0)

    def choose_action(self, current_room):
        # If the random number is less than epsilon, then choose a random action
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        # Else choose the action with the highest Q-value
        else:
            max_q_value = max([self.get_q_value(current_room, a)
                              for a in self.actions])
            best_actions = [a for a in self.actions if self.get_q_value(
                current_room, a) == max_q_value]

            if not best_actions:
                return random.choice(self.actions)

        return random.choice(best_actions)

    def learn(self, current_room, action, reward, next_room):
        # Q-value update formula
        current_q = self.get_q_value(current_room, action)
        max_future_q = max([self.get_q_value(next_room, a)
                           for a in self.actions])
        new_q = current_q + self.learning_rate * \
            (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[(current_room, action)] = new_q
