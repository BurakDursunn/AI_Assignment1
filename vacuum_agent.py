import random


class VacuumAgent:
    def __init__(self, agent_name):
        # Room object with type Room
        self.current_room = None
        self.current_score = 0.0
        self.agent_name = agent_name

    # Decide the action for the agent, for left and right, if room is A only go right, if room is B go left or right, if room is C only go left
    def decide_action(self):
        # Get the current room for the agent
        current_room = self.current_room

        actions = ['suck', 'no-op']

        if current_room.get_room_letter() == 'A':
            actions.append('right')
        elif current_room.get_room_letter() == 'B':
            actions.append('left')
            actions.append('right')
        elif current_room.get_room_letter() == 'C':
            actions.append('left')

        # Decide the action for the agent
        return random.choice(actions)

    # Getters and setters
    def get_current_room(self):
        return self.current_room

    def set_current_room(self, room):
        self.current_room = room

    def get_current_score(self):
        return self.current_score

    def set_current_score(self, score):
        self.current_score = score

    def get_agent_name(self):
        return self.agent_name

    def set_agent_name(self, name):
        self.agent_name = name
