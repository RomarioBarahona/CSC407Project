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
initial_theta = 0.7  # Initial vaccine effectiveness (0 < theta < 1)

# Create community assignments for each individual
community_assignments = [random.randint(0, K - 1) for _ in range(N)]

# Create a random graph using G(n, p) model for social connections
G = nx.gnp_random_graph(N, 0.2)  # Adjust p as needed

# Step 2 to 4: Simulate the spread of the pandemic
T = 2000  # Total rounds

# List of vaccination rates (v) to explore
vaccination_rates = [i / 100 for i in range(101)]  # 0% to 100%

# List of theta decrease rates to explore
theta_decrease_rates = [0.01, 0.02, 0.03]  # Rate of θ decrease per round

# Initialize lists to store total infections for different rates of θ decrease
total_infections_lists = [[] for _ in range(len(theta_decrease_rates))]

for theta_decrease_index, theta_decrease_rate in enumerate(theta_decrease_rates):
    infected_copy = infected.copy()
    total_infected = [1]  # List to store the number of infected individuals after each round
    theta = initial_theta  # Initial vaccine effectiveness

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

        # Decrease theta by the specified rate
        theta -= theta_decrease_rate

        # Ensure theta does not go below zero
        theta = max(theta, 0)

    # Record the total infections for this θ decrease rate
    total_infections_lists[theta_decrease_index] = total_infected[1:]  # Exclude the initial infected person

# Plot the results for different θ decrease rates
for i, theta_decrease_rate in enumerate(theta_decrease_rates):
    plt.plot(range(1, T), total_infections_lists[i], label=f'Theta Decrease Rate = {theta_decrease_rate}')

plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Total Infection vs. Rounds with Vaccine Wear-off')
plt.legend()
plt.grid(True)
plt.show()
