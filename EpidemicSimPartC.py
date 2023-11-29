import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, vaccine_round, vaccine_efficiency, vaccination_rate):
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
        if round == vaccine_round:
            # Introduce the vaccine for a fraction of the population
            vaccinated = random.sample(range(N), int(vaccination_rate * N))
            for v in vaccinated:
                initial_infected[v] = False  # Vaccinated individuals are immune

        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(range(N), int(alpha * N))
                for j in contacts:
                    if not initial_infected[j]:
                        # Apply vaccine effect
                        if round >= vaccine_round:
                            if random.random() < beta * (1 - vaccine_efficiency):
                                initial_infected[j] = True
                                new_infections += 1
                        else:
                            if random.random() < beta:
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
T = 2000  # Total rounds
vaccine_round = 100  # Round at which the vaccine is introduced
vaccine_efficiency = 0.95  # Vaccine effectiveness (95%)

# Define different vaccination rates to simulate
vaccination_rates = [0.2, 0.4, 0.6, 0.8, 1.0]  # Varying rates (e.g., 20%, 40%, 60%, 80%, 100%)

# Run simulations for different vaccination rates
results = []
for rate in vaccination_rates:
    total_infected, _, _, _ = simulate_pandemic(alpha, beta, t1, t2, T, vaccine_round, vaccine_efficiency, rate)
    results.append(total_infected)

# Plot the results for total infected with different vaccination rates
plt.figure(figsize=(12, 6))
for i, rate in enumerate(vaccination_rates):
    plt.plot(range(T), results[i], label=f'Vaccination Rate {int(rate*100)}%')

plt.ylabel('Total Infected')
plt.title('Total Infected Individuals with Different Vaccination Rates')
plt.legend()
plt.show()
