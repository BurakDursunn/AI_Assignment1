import random
import time
import os
from VacuumAI import VacuumAI
from vacuum_agent import VacuumAgent
from room import Room


def main(PA, PB, PC, num_simulations, num_steps, configuration):
    # Create the agents
    agent_A = VacuumAgent(agent_name="A")
    agent_B = VacuumAgent(agent_name="B")

    results_for_agent_A = []
    results_for_agent_B = []

    # Run the simulation for each agent
    run_simulation_for_agent(
        agent_A, PA, PB, PC, num_simulations, num_steps, configuration, results_for_agent_A)
    run_simulation_for_agent(
        agent_B, PA, PB, PC, num_simulations, num_steps, configuration, results_for_agent_B)

    # Calculate the average score for each agent
    average_score_A = sum(results_for_agent_A) / len(results_for_agent_A)
    average_score_B = sum(results_for_agent_B) / len(results_for_agent_B)

    # Print the average score for each agent
    print("Average score for agent A: {}\n".format(average_score_A))
    print("Average score for agent B: {}\n".format(average_score_B))

    # Write the average score for each agent to a file
    with open("output/average_score.txt", "a") as f:
        f.write("Configuration #{}\n".format(configuration))
        f.write("Average score for agent A: {}\n".format(average_score_A))
        f.write("Average score for agent B: {}\n".format(average_score_B))
        f.write("\n")


def run_simulation_for_agent(agent, PA, PB, PC, num_simulations, num_steps, configuration, results):
    # Run the simulation num_simulations times
    for i in range(num_simulations):
        # Reset random seed
        random.seed(int(time.time()))

        print("Simulation #{} for agent {} with configuration #{}\n".format(
            i + 1, agent.get_agent_name(), configuration))
        # Create the rooms
        room_A = Room(is_dirty=True, room_letter="A",
                      neighbor_rooms=["B"], dirt_prob=PA)
        room_B = Room(is_dirty=True, room_letter="B",
                      neighbor_rooms=["A", "C"], dirt_prob=PB)
        room_C = Room(is_dirty=True, room_letter="C",
                      neighbor_rooms=["B"], dirt_prob=PC)

        # Initialy set the agent to room B
        agent.set_current_room(room_B)

        # Create QLearningAI object
        vacuum_ai = VacuumAI(learning_rate=0.1, exploration_prob=0.1,
                             discount_factor=0.6)

        file_name = "output/agent_{}_configuration_{}_simulation_{}.txt".format(
            agent.get_agent_name(), configuration, i + 1)

        # print("File name: {}\n".format(file_name))

        # Write the simulation number to a file with the syntax "Simulation #1" and recreate the file if it already exists
        with open(file_name, "w") as f:
            f.write("Simulation #{} for agent {} with configuration #{}\n\n".format(
                i + 1, agent.get_agent_name(), configuration))

        # Run the simulation num_steps times
        for step in range(num_steps):
            run_simulation(agent, room_A, room_B, room_C,
                           step, file_name, vacuum_ai)

        # print("Simulation #{} complete\n".format(i + 1))
        print("Agent {} score: {}\n".format(
            agent.get_agent_name(), agent.get_current_score()))

        # Save the agent's score to a list
        results.append(agent.get_current_score())

        # Reset the agent's score and room
        agent.set_current_score(0.0)
        agent.set_current_room(None)


def run_simulation(agent, room_A, room_B, room_C, step, file_name, vacuum_ai):

    # Get the current state of the rooms
    current_step = step + 1

    # print("Step {}\n".format(current_step))

    # Get the current room for the agent and the room states, syntax string "agent.current_room, room_A.is_dirty, room_B.is_dirty, room_C.is_dirty" and save it to a variable called "current_state" (hint: use the format method)
    current_state = "{}, {}, {}, {}".format(agent.get_current_room(
    ).get_room_letter(), room_A.room_dirty(), room_B.room_dirty(), room_C.room_dirty())

    # print("{}\n".format(current_state))

    # Decide the action for the agent using the RewardBasedAI object
    current_room = agent.get_current_room().get_room_letter()
    action = vacuum_ai.decide_action(
        current_room, agent.get_current_room().get_is_dirty())

    # print("{}\n".format(action))

    # Update the room states based on the action
    update_room_states(action, agent, room_A, room_B, room_C)

    # Update the Q-values using the RewardBasedAI object
    reward = agent.get_current_score()
    next_room = agent.get_current_room().get_room_letter()
    vacuum_ai.update_q_values(current_room, next_room,
                              action, reward, agent.get_agent_name())

    # Get updated state of the rooms and agent, syntax string "agent.current_room, room_A.is_dirty, room_B.is_dirty, room_C.is_dirty"
    updated_state = "{}, {}, {}, {}".format(agent.get_current_room(
    ).get_room_letter(), room_A.room_dirty(), room_B.room_dirty(), room_C.room_dirty())

    # print("{}\n".format(updated_state))

    # Get Score
    score = agent.current_score

    # print("{}\n".format(score))

    # Decide dirtiness of rooms
    room_A.update_dirt()
    room_B.update_dirt()
    room_C.update_dirt()

    # Write the current state, action, updated state, and score to a file
    with open(file_name, "a") as f:
        f.write("Step {}\n\n".format(current_step))
        f.write("Current state: {}\n\n".format(current_state))
        f.write("Action: {}\n\n".format(action))
        f.write("Updated state: {}\n\n".format(updated_state))
        f.write("Score: {}\n\n".format(score))


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
    calculate_points(agent, room_A, room_B, room_C, action)


def calculate_points(agent, room_A, room_B, room_C, action):
    points = 0.0
    # Calculate points for each agent, If the agent is A score system is get 1 point for each clean room, if the agent is B score system is get 1 point for each clean room and for left and right actions get -0.5 points
    if agent.get_agent_name() == "A":
        if not room_A.get_is_dirty():
            points += 1
        if not room_B.get_is_dirty():
            points += 1
        if not room_C.get_is_dirty():
            points += 1
    elif agent.get_agent_name() == "B":
        if not room_A.get_is_dirty():
            points += 1
        if not room_B.get_is_dirty():
            points += 1
        if not room_C.get_is_dirty():
            points += 1
        if action == "left" or action == "right":
            points -= 0.5

    agent.set_current_score(agent.get_current_score() + points)


if __name__ == "__main__":
    random.seed(int(time.time()))

    CONFIGURATION = {
        "Probilities": [
            {
                "PA": 0.3,
                "PB": 0.3,
                "PC": 0.3,
            },
            {
                "PA": 0.5,
                "PB": 0.2,
                "PC": 0.1,
            },
            {
                "PA": 0.2,
                "PB": 0.4,
                "PC": 0.2,
            },
            {
                "PA": 0.5,
                "PB": 0.1,
                "PC": 0.3,
            },
            {
                "PA": 0.5,
                "PB": 0.3,
                "PC": 0.8,
            }
        ],
        "NumSimulations": 10,
        "NumSteps": 1000
    }

    configuration = 1

    # Create output directory if it doesn't exist
    if not os.path.exists("output"):
        os.makedirs("output")

    # Create the reslt file
    with open("output/average_score.txt", "w") as f:
        f.write("Results\n\n")

    for config in CONFIGURATION["Probilities"]:
        # Reset random seed
        random.seed(int(time.time()))

        print("Configuration #{}\n".format(configuration))

        main(config["PA"], config["PB"], config["PC"],
             CONFIGURATION["NumSimulations"], CONFIGURATION["NumSteps"], configuration)

        configuration += 1
