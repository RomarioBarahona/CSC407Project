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
gamma = 0.2  # Ratio of social connections to interact with
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
t3 = 1000  # Round at which vaccine is introduced
theta = 0.7  # Vaccine effectiveness (0 < theta < 1)

# Create community assignments for each individual
community_assignments = [random.randint(0, K - 1) for _ in range(N)]

# Create a random graph using G(n, p) model for social connections
G = nx.gnp_random_graph(N, 0.2)  # Adjust p as needed

# Step 2 to 4: Simulate the spread of the pandemic
T = 2000  # Total rounds

# List of vaccination rates (v) to explore
vaccination_rates = [i / 100 for i in range(101)]  # 0% to 100%
total_infections = []  # List to store total infections for each vaccination rate

for v in vaccination_rates:
    infected_copy = infected.copy()
    total_infected = [1]  # List to store the number of infected individuals after each round
    for round in range(1, T):
        new_infections = 1  # Initialize with 1 for the initial infected person
        for i in range(N):
            if infected_copy[i]:
                social_connections = list(G.neighbors(i))
                num_contacts = int(gamma * len(social_connections))
                contacts = random.sample(social_connections, num_contacts)
                for j in contacts:
                    if not infected_copy[j] and random.random() < beta:
                        infected_copy[j] = True
                        new_infections += 1

        # Step 5: Introduce the vaccine at t3 round
        if round == t3:
            for i in range(N):
                if random.random() < theta:
                    infected_copy[i] = False

        total_infected.append(total_infected[-1] + new_infections)

    # Record the total infections for this vaccination rate
    total_infections.append(total_infected[-1])

# Plot the results
plt.plot(vaccination_rates, total_infections)
plt.xlabel('Vaccination Rate (v)')
plt.ylabel('Total Infected')
plt.title('Total Infection vs. Vaccination Rate')
plt.xlim(0, 1)
plt.grid(True)
plt.show()
