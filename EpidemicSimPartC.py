import random
import matplotlib.pyplot as plt
import networkx as nx

# Step 1: Initialize the simulation
N = 1000  # Number of people
K = 10  # Number of communities
b = 20  # Number of bridge individuals
infected = [False] * N  # Array to record infection status
infected[0] = True  # Initial infected person
total_infected = [1]  # List to store the number of infected individuals after each round

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
for round in range(1, T):
    new_infections = 1  # Initialize with 1 for the initial infected person
    for i in range(N):
        if infected[i]:
            social_connections = list(G.neighbors(i))
            num_contacts = int(gamma * len(social_connections))
            contacts = random.sample(social_connections, num_contacts)
            for j in contacts:
                if not infected[j] and random.random() < beta:
                    infected[j] = True
                    new_infections += 1

    # Step 5: Introduce the vaccine at t3 round
    if round == t3:
        for i in range(N):
            if random.random() < theta:
                infected[i] = False

    # Step 5: Record the number of infected individuals
    total_infected.append(total_infected[-1] + new_infections)

# Vaccination rates for two communities
v1 = 0.5
v2 = 0.85

# Calculate the number of vaccinated individuals in each community
num_vaccinated_community1 = int(N * v1)
num_vaccinated_community2 = int(N * v2)

# Apply vaccination to individuals in the respective communities
for i in range(N):
    if community_assignments[i] == 0 and num_vaccinated_community1 > 0:
        if random.random() < v1:
            infected[i] = False
            num_vaccinated_community1 -= 1
    elif community_assignments[i] == 1 and num_vaccinated_community2 > 0:
        if random.random() < v2:
            infected[i] = False
            num_vaccinated_community2 -= 1

# Plot the results
plt.plot(range(T), total_infected)
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread with Vaccination in Communities')
plt.show()

# Step 6: Calculate R0 for step 6
R0_step6 = total_infected[t1] / total_infected[0]

# Step 7: Calculate R0 for step 7
R0_step7 = total_infected[t1 + t2] / total_infected[0]

print(f'R0 for step 6: {R0_step6}')
print(f'R0 for step 7: {R0_step7}')
