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

    def decide_action(self, current_room, is_dirty):
        # Decide the action for the agent using numpy
        if np.random.random() < self.exploration_prob:
            decided_action = ""
            # Explore: Choose a random action
            if current_room == "A":
                decided_action = np.random.choice(["suck", "no-op", "right"])
                if decided_action == "no-op" and is_dirty:
                    decided_action = "suck"
                elif decided_action == "suck" and not is_dirty:
                    decided_action = "no-op"
                return decided_action
            elif current_room == "B":
                decided_action = np.random.choice(
                    ["suck", "no-op", "left", "right"])
                if decided_action == "no-op" and is_dirty:
                    decided_action = "suck"
                elif decided_action == "suck" and not is_dirty:
                    decided_action = "no-op"
                return decided_action
            elif current_room == "C":
                decided_action = np.random.choice(["suck", "no-op", "left"])
                if decided_action == "no-op" and is_dirty:
                    decided_action = "suck"
                elif decided_action == "suck" and not is_dirty:
                    decided_action = "no-op"
                return decided_action
        else:
            decided_action = ""
            # Exploit: Choose the action with the highest Q value
            if current_room == "A":
                decided_action = self.enum_to_str(
                    np.argmax(self.q_values[enum_room["A"]]), "action")
            elif current_room == "B":
                decided_action = self.enum_to_str(
                    np.argmax(self.q_values[enum_room["B"]]), "action")
            elif current_room == "C":
                decided_action = self.enum_to_str(
                    np.argmax(self.q_values[enum_room["C"]]), "action")

            if decided_action == "suck" and not is_dirty:
                decided_action = "no-op"
            elif decided_action == "no-op" and is_dirty:
                decided_action = "suck"
            return decided_action

    def update_q_values(self, current_room, next_room, action, reward, agent_name):
        # If agent is B, then update the q values, else icrement punishment
        reward_q = reward
        if agent_name == "B":
            if action == "left" or action == "right":
                reward_q = reward - 0.5
            else:
                reward_q = reward
        current_q = self.q_values[enum_room[current_room]][enum_action[action]]
        best_next_q = max(self.q_values[enum_room[next_room]])
        self.q_values[enum_room[current_room]][enum_action[action]] = current_q + self.learning_rate * (
            reward_q + self.discount_factor * best_next_q - current_q)

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
