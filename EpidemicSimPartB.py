import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, gamma, t1, t2, T):
    # Initialize the simulation
    N = 1000  # Number of people
    connections = {}  # Dictionary to store fixed connections for each individual

    # Generate fixed connections for each individual using G(n, p)
    for i in range(N):
        connections[i] = set()
        for j in range(N):
            if i != j and random.random() < alpha:
                connections[i].add(j)

    initial_infected = [False] * N
    total_infected = [0] * T
    new_infections_per_round = [0] * T  # Store new infections per round

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
                contacts = random.sample(list(connections[i]), int(gamma * len(connections[i])))
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

# Parameters
alpha = 0.1  # Probability of a connection in G(n, p)
beta = 0.01  # Infection probability
gamma_values = [0.1, 0.2, 0.3, 0.4, 0.5]  # Varying contact ratios (γ)
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
T = 500  # Total rounds

# Run simulations for different contact ratios (γ)
results = []
for gamma in gamma_values:
    total_infected, _, _, _ = simulate_pandemic(alpha, beta, gamma, t1, t2, T)
    results.append(total_infected)

# Plot the results for total infected with different contact ratios (γ)
plt.figure(figsize=(12, 6))
for i, gamma in enumerate(gamma_values):
    plt.plot(range(T), results[i], label=f'Contact Ratio (γ) = {gamma}')

plt.ylabel('Total Infected')
plt.title('Total Infected Individuals with Different Contact Ratios (γ)')
plt.legend()
plt.show()
