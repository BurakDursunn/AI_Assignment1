import numpy as np

enum_room = {
    "A": 0,
    "B": 1,
    "C": 2
}

enum_action = {
    "suck": 0,
    "no-op": 1,
    "left": 2,
    "right": 3
}


class VacuumAI:

    def __init__(self, learning_rate, exploration_prob, discount_factor):
        self.learning_rate = learning_rate
        self.exploration_prob = exploration_prob
        self.discount_factor = discount_factor
        self.q_values = np.zeros((3, 4))

    def decide_action(self, current_room):
        # Decide the action for the agent using numpy
        if np.random.random() < self.exploration_prob:
            # Explore: Choose a random action
            if current_room == "A":
                return np.random.choice(["suck", "no-op", "right"])
            elif current_room == "B":
                return np.random.choice(["suck", "no-op", "left", "right"])
            elif current_room == "C":
                return np.random.choice(["suck", "no-op", "left"])
        else:
            # Exploit: Choose the action with the highest Q value
            if current_room == "A":
                return self.enum_to_str(np.argmax(self.q_values[enum_room["A"]]), "action")
            elif current_room == "B":
                return self.enum_to_str(np.argmax(self.q_values[enum_room["B"]]), "action")
            elif current_room == "C":
                return self.enum_to_str(np.argmax(self.q_values[enum_room["C"]]), "action")

    def update_q_values(self, current_room, next_room, action, reward):
        current_q = self.q_values[enum_room[current_room]][enum_action[action]]
        best_next_q = max(self.q_values[enum_room[next_room]])
        self.q_values[enum_room[current_room]][enum_action[action]] = current_q + self.learning_rate * (
            reward + self.discount_factor * best_next_q - current_q)

    def enum_to_str(self, num, type):
        if type == "room":
            if num == enum_room["A"]:
                return "A"
            elif num == enum_room["B"]:
                return "B"
            elif num == enum_room["C"]:
                return "C"
        elif type == "action":
            if num == enum_action["suck"]:
                return "suck"
            elif num == enum_action["no-op"]:
                return "no-op"
            elif num == enum_action["left"]:
                return "left"
            elif num == enum_action["right"]:
                return "right"
