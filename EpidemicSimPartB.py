import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread in a network with fixed connections
def simulate_pandemic_with_fixed_connections(alpha, beta, T, num_connections):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T

    # Create a network where each person has a fixed set of connections
    network = {}
    for i in range(N):
        network[i] = random.sample(range(N), num_connections)  # Randomly choose num_connections connections

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(network[i], int(alpha * num_connections))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        initial_infected[j] = True
                        new_infections += 1
        
        total_infected[round] = total_infected[round - 1] + new_infections

    return total_infected

# Parameters
alpha = 0.05       # Ratio of contacts
beta = 0.01      # Infection probability
T = 2000         # Total rounds
num_connections = 20  # Number of fixed connections for each person

# Run the simulation with fixed connections
total_infected = simulate_pandemic_with_fixed_connections(alpha, beta, T, num_connections)

# Plot the results
plt.plot(range(T), total_infected)
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread with Fixed Connections')
plt.show()
