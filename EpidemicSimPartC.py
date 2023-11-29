import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, vaccine_rounds, vaccination_rate):
    # Initialize the simulation
    N = 1000  # Number of people
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
        if round in vaccine_rounds:
            # Introduce the vaccine gradually for a fraction of the population
            vaccinated = random.sample(range(N), int(vaccination_rate * N))
            for v in vaccinated:
                initial_infected[v] = False  # Vaccinated individuals are immune

        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(range(N), int(alpha * N))
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
alpha = 0.005  # Ratio of contacts
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
T = 500  # Total rounds
vaccine_rounds = list(range(250, 301))  # Rounds at which the vaccine is introduced
vaccination_rate = 0.8  # Fraction of the population that will take the vaccine

# Run the simulation
total_infected, new_infections_per_round, R0_step6, R0_step7 = simulate_pandemic(alpha, beta, t1, t2, T, vaccine_rounds, vaccination_rate)

# Plot the results for total infected
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.plot(range(T), total_infected, label='Total Infected')
plt.ylabel('Total Infected')
plt.title('Total Infected Individuals')

# Plot the results for new infections per round
plt.subplot(2, 1, 2)
plt.plot(range(T), new_infections_per_round, label='New Infections per Round')
plt.xlabel('Rounds')
plt.ylabel('New Infections per Round')
plt.title('New Infections per Round')

plt.tight_layout()
plt.show()

# Print R0 values for the simulation
print(f'R0 for step 6: {R0_step6}')
print(f'R0 for step 7: {R0_step7}')
