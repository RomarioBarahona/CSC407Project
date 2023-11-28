import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(range(N), int(alpha * N))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        initial_infected[j] = True
                        new_infections += 1
        
        total_infected[round] = total_infected[round - 1] + new_infections

    # Calculate R0 for step 6
    R0_step6 = total_infected[t1] / total_infected[0]

    # Calculate R0 for step 7
    R0_step7 = total_infected[t1 + t2] / total_infected[0]

    return total_infected, R0_step6, R0_step7

# Parameters
alpha = 0.005  # Ratio of contacts
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
T = 2000  # Total rounds

# Run the simulation 5 times
for i in range(5):
    total_infected, R0_step6, R0_step7 = simulate_pandemic(alpha, beta, t1, t2, T)

    # Plot the results
    plt.plot(range(T), total_infected, label=f'Simulation {i+1}')

# Customize the plot
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread (5 Simulations)')
plt.legend()
plt.show()

# Print R0 values for the last simulation
print(f'R0 for step 6 (last simulation): {R0_step6}')
print(f'R0 for step 7 (last simulation): {R0_step7}')
