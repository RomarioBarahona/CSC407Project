import random
import matplotlib.pyplot as plt
import numpy as np

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, num_connections, contact_ratio):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T
    new_infections_per_round = [0] * T  # Store new infections per round

    # Create a social network (fixed connections)
    social_network = {}
    for i in range(N):
        social_network[i] = random.sample(range(N), num_connections)

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1
    new_infections_per_round[0] = 1

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(social_network[i], int(contact_ratio * num_connections))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        initial_infected[j] = True
                        new_infections += 1
        
        new_infections_per_round[round] = new_infections
        total_infected[round] = total_infected[round - 1] + new_infections

    # Calculate R0 for step 6
    R0_step6 = new_infections_per_round[t1] / new_infections_per_round[0]

    # Calculate R0 for step 7
    R0_step7 = new_infections_per_round[t1 + t2] / new_infections_per_round[0]

    return total_infected, new_infections_per_round, R0_step6, R0_step7

# Function to simulate the effect of vaccination
def simulate_vaccination(alpha, beta, t1, t2, T, num_connections, contact_ratio, vaccination_rate):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T
    new_infections_per_round = [0] * T  # Store new infections per round

    # Create a social network (fixed connections)
    social_network = {}
    for i in range(N):
        social_network[i] = random.sample(range(N), num_connections)

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1
    new_infections_per_round[0] = 1

    # Simulate the spread of the pandemic with vaccination
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(social_network[i], int(contact_ratio * num_connections))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        if random.random() > vaccination_rate:
                            initial_infected[j] = True
                            new_infections += 1
        
        new_infections_per_round[round] = new_infections
        total_infected[round] = total_infected[round - 1] + new_infections

    return total_infected

# Parameters
alpha = 0.005  # Ratio of contacts
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
T = 2000  # Total rounds
num_connections = 20  # Number of fixed social connections per individual
contact_ratio = 0.2  # Ratio of contacts in each infection round

# Ensure that all simulations run for the same number of rounds (T)
common_T = T

# Simulate pandemic spread with different contact ratios
contact_ratios = [0.1, 0.2, 0.3]
total_infections_by_contact_ratio = []

for contact_ratio in contact_ratios:
    total_infected = simulate_pandemic(alpha, beta, t1, t2, common_T, num_connections, contact_ratio)
    total_infections_by_contact_ratio.append(total_infected)

# Plot total infections as a function of contact ratio
plt.figure(figsize=(10, 6))
for i, contact_ratio in enumerate(contact_ratios):
    plt.plot(range(common_T), total_infections_by_contact_ratio[i][0:common_T], label=f'Contact Ratio {contact_ratio}')
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Total Infections vs. Contact Ratio')
plt.legend()
plt.show()

# Simulate the effect of vaccination with different vaccination rates
vaccination_rates = [0.2, 0.5, 0.8]
total_infections_by_vaccination_rate = []

for vaccination_rate in vaccination_rates:
    total_infected = simulate_vaccination(alpha, beta, t1, t2, common_T, num_connections, contact_ratio, vaccination_rate)
    total_infections_by_vaccination_rate.append(total_infected)

# Plot total infections as a function of vaccination rate
plt.figure(figsize=(10, 6))
for i, vaccination_rate in enumerate(vaccination_rates):
    plt.plot(range(common_T), total_infections_by_vaccination_rate[i][0:common_T], label=f'Vaccination Rate {vaccination_rate}')
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Total Infections vs. Vaccination Rate')
plt.legend()
plt.show()
