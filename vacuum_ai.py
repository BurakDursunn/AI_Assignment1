import random


class VacuumAi:
    def __init__(self):
        self.roomA_dirty_prob = 1.0
        self.roomB_dirty_prob = 1.0
        self.roomC_dirty_prob = 1.0
        self.dirty_counters = {
            "A": 0,
            "B": 0,
            "C": 0
        }

    def guess_room_dirty_prob(self, roomA, roomB, roomC):
        for room in [roomA, roomB, roomC]:
            room_letter = room.get_room_letter()
            dirty_prob = self.roomA_dirty_prob if room_letter == "A" else self.roomB_dirty_prob if room_letter == "B" else self.roomC_dirty_prob

            if room.get_is_dirty():
                dirty_counter = self.dirty_counters[room_letter]
                dirty_counter += 1
                self.dirty_counters[room_letter] = dirty_counter
            else:
                dirty_counter = self.dirty_counters[room_letter]
                if dirty_counter > 0:
                    new_dirty_prob = 1 / (dirty_counter + 1)
                    dirty_prob = (dirty_prob + new_dirty_prob) / 2
                    self.dirty_counters[room_letter] = 0

            if room_letter == "A":
                self.roomA_dirty_prob = dirty_prob
            elif room_letter == "B":
                self.roomB_dirty_prob = dirty_prob
            elif room_letter == "C":
                self.roomC_dirty_prob = dirty_prob

    def get_room_dirty_prob(self, room):
        room_letter = room.get_room_letter()
        dirty_prob = self.roomA_dirty_prob if room_letter == "A" else self.roomB_dirty_prob if room_letter == "B" else self.roomC_dirty_prob
        return dirty_prob

    def decide_action(self, agent, room_A, room_B, room_C):
        # Two different vacuum AI's one for agent A and one for agent B

        # Get name of agent
        agent_name = agent.get_agent_name()

        if agent_name == "A":
            return self.decide_action_A(agent)
        elif agent_name == "B":
            return self.decide_action_B(agent, room_A, room_B, room_C)

    def decide_action_A(self, agent):
        actions = []

        current_room = agent.get_current_room()

        if current_room.get_is_dirty():
            actions.append("suck")
        else:
            actions.append("no-op")

        return random.choice(actions)

    def decide_action_B(self, agent, room_A, room_B, room_C):
        actions = []
        current_room = agent.get_current_room()
        current_room_prob = self.get_room_dirty_prob(current_room)

        if current_room_prob > 0.5 and current_room.get_is_dirty():
            actions.append("suck")
        else:
            if current_room.get_room_letter() == "A":
                actions.append("right")
            elif current_room.get_room_letter() == "B":
                actions.append("left")
                actions.append("right")
            elif current_room.get_room_letter() == "C":
                actions.append("left")
            actions.append("no-op")

        return random.choice(actions)

    """def decide_action(self, agent, room_A, room_B, room_C):
        actions = []
        current_room = agent.get_current_room()
        current_room_prob = self.get_room_dirty_prob(current_room)

        if current_room_prob > 0.5 and current_room.get_is_dirty():
            actions.append("suck")
        else:
            if current_room.get_room_letter() == "A":
                actions.append("right")
            elif current_room.get_room_letter() == "B":
                actions.append("left")
                actions.append("right")
            elif current_room.get_room_letter() == "C":
                actions.append("left")
            actions.append("no-op")

        return random.choice(actions)"""
