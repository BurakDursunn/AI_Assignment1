import random
import time
from vacuum_agent import VacuumAgent
from room import Room


def main(PA, PB, PC, num_simulations=10, num_steps=1000):
    # Create the agents
    agent_A = VacuumAgent(agent_name="A")
    agent_B = VacuumAgent(agent_name="B")

    # Run the simulation for each agent
    run_simulation_for_agent(agent_A, num_simulations, num_steps, "a.txt")
    run_simulation_for_agent(agent_B, num_simulations, num_steps, "b.txt")


def run_simulation_for_agent(agent, num_simulations=10, num_steps=1000, file_name=""):
    # Run the simulation num_simulations times
    for i in range(num_simulations):
        print("Simulation #{}".format(i + 1))
        # Create the rooms
        room_A = Room(is_dirty=True, room_letter="A",
                      neighbor_rooms=["B"], dirt_prob=PA)
        room_B = Room(is_dirty=True, room_letter="B",
                      neighbor_rooms=["A", "C"], dirt_prob=PB)
        room_C = Room(is_dirty=True, room_letter="C",
                      neighbor_rooms=["B"], dirt_prob=PC)

        # Initialy set the agent to room B
        agent.set_current_room(room_B)

        file_name = "agent_{}_simulation_{}.txt".format(
            agent.get_agent_name(), i + 1)

        # Write the simulation number to a file with the syntax "Simulation #1" and recreate the file if it already exists
        with open(file_name, "a") as f:
            f.write("Simulation #{}\n".format(i + 1))

        # Run the simulation num_steps times
        for step in range(num_steps):
            run_simulation(agent, room_A, room_B, room_C, step, file_name)

        # Reset the agent's score and room
        agent.set_current_score(0)
        agent.set_current_room(None)


def run_simulation(agent, room_A, room_B, room_C, step, file_name):

    # Get the current state of the rooms
    current_step = step + 1

    print("Step {}\n".format(current_step))

    # Get the current room for the agent and the room states, syntax string "agent.current_room, room_A.is_dirty, room_B.is_dirty, room_C.is_dirty" and save it to a variable called "current_state" (hint: use the format method)
    current_state = "{}, {}, {}, {}".format(agent.get_current_room(
    ).get_room_letter(), room_A.room_dirty(), room_B.room_dirty(), room_C.room_dirty())

    print("{}\n".format(current_state))

    # Decide the action for the agent
    action = agent.decide_action()

    print("{}\n".format(action))

    # Update the room states based on the action
    update_room_states(action, agent, room_A, room_B, room_C)

    # Get updated state of the rooms and agent, syntax string "agent.current_room, room_A.is_dirty, room_B.is_dirty, room_C.is_dirty"

    updated_state = "{}, {}, {}, {}".format(agent.get_current_room(
    ).get_room_letter(), room_A.room_dirty(), room_B.room_dirty(), room_C.room_dirty())

    print("{}\n".format(updated_state))

    # Get Score
    score = agent.current_score

    print("{}\n".format(score))

    # Decide dirtiness of rooms
    room_A.update_dirt()
    room_B.update_dirt()
    room_C.update_dirt()

    # Write the current state, action, updated state, and score to a file
    with open(file_name, "a") as f:
        f.write("Step {}\n\n".format(current_step))
        f.write("{}\n\n".format(current_state))
        f.write("{}\n\n".format(action))
        f.write("{}\n\n".format(updated_state))
        f.write("{}\n\n".format(score))


def update_room_states(action, agent, room_A, room_B, room_C):
    # Get the current room for the agent
    current_room = agent.get_current_room()

    # If the action is suck, then clean the room
    if action == "suck":
        current_room.set_is_dirty(False)
    # If the action is right, then move to the right room
    elif action == "right":
        if current_room == room_A:
            agent.current_room = room_B
        elif current_room == room_B:
            agent.current_room = room_C
    # If the action is left, then move to the left room
    elif action == "left":
        if current_room == room_B:
            agent.current_room = room_A
        elif current_room == room_C:
            agent.current_room = room_B
    # If the action is no-op, then do nothing
    elif action == "no-op":
        pass

    # Update the agent's score, If the agent is A score system is get 1 point for each clean room, if the agent is B score system is get 1 point for each clean room and for left and right actions get -0.5 points
    if agent.get_agent_name() == "A":
        if not room_A.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
        if not room_B.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
        if not room_C.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
    elif agent.get_agent_name() == "B":
        if not room_A.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
        if not room_B.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
        if not room_C.get_is_dirty():
            agent.set_current_score(agent.get_current_score() + 1)
        if action == "left" or action == "right":
            agent.set_current_score(agent.get_current_score() - 0.5)


if __name__ == "__main__":
    random.seed(int(time.time()))

    # Get PA, PB, and PC from user input
    PA = float(input("Enter probability of room A being dirty: "))
    PB = float(input("Enter probability of room B being dirty: "))
    PC = float(input("Enter probability of room C being dirty: "))

    main(PA, PB, PC)
