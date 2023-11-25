import random
import matplotlib.pyplot as plt
import networkx as nx

# Step 1: Initialize the simulation
N = 1000  # Number of people
K = 10  # Number of communities
b = 20  # Number of bridge individuals
infected = [False] * N  # Array to record infection status
infected[0] = True  # Initial infected person

# Parameters
gamma = 0.2  # Ratio of social connections to interact with (normal social activity)
game_connections_factor = 5  # Increase connections during the game
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity

# Create community assignments for each individual
community_assignments = [random.randint(0, K - 1) for _ in range(N)]

# Create a random graph using G(n, p) model for social connections during normal social activity
G_normal = nx.gnp_random_graph(N, gamma)  # Normal social connections

# Create a random graph with additional connections during the game
G_game = nx.gnp_random_graph(N, gamma * game_connections_factor)  # Connections during the game

# Step 2 to 4: Simulate the spread of the pandemic during normal social activity
T = 2000  # Total rounds
total_infected_normal = [1]  # List to store the number of infected individuals during normal activity

for round in range(1, T):
    new_infections = 1  # Initialize with 1 for the initial infected person
    for i in range(N):
        if infected[i]:
            social_connections = list(G_normal.neighbors(i))
            num_contacts = int(gamma * len(social_connections))
            contacts = random.sample(social_connections, num_contacts)
            for j in contacts:
                if not infected[j] and random.random() < beta:
                    infected[j] = True
                    new_infections += 1

    total_infected_normal.append(total_infected_normal[-1] + new_infections)

# Reset infected status for the game simulation
infected = [False] * N
infected[0] = True

# Step 2 to 4: Simulate the spread of the pandemic during the game
total_infected_game = [1]  # List to store the number of infected individuals during the game

for round in range(1, T):
    new_infections = 1  # Initialize with 1 for the initial infected person
    for i in range(N):
        if infected[i]:
            social_connections = list(G_game.neighbors(i))
            num_contacts = int(gamma * game_connections_factor * len(social_connections))
            contacts = random.sample(social_connections, num_contacts)
            for j in contacts:
                if not infected[j] and random.random() < beta:
                    infected[j] = True
                    new_infections += 1

    total_infected_game.append(total_infected_game[-1] + new_infections)

# Plot the results for comparison
plt.plot(range(T), total_infected_normal, label='Normal Social Activity')
plt.plot(range(T), total_infected_game, label='During Football/Basketball Game (5x connections)')
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread Comparison: Normal vs. Game')
plt.legend()
plt.grid(True)
plt.show()
