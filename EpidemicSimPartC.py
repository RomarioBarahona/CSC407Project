import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, num_social_connections, social_ratio, vaccine_round, vaccine_efficacy, vaccination_rate):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T

    # Create a list of social connections for each individual
    social_connections = []
    for i in range(N):
        # Randomly select social connections for each individual
        connections = random.sample(range(N), num_social_connections)
        social_connections.append(connections)

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1

    # Lists to keep track of vaccination status, efficacy, and rate
    vaccinated = [False] * N
    vaccine_effective = [False] * N
    vaccination_started = False

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(social_connections[i], int(social_ratio * num_social_connections))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        if vaccination_started and vaccinated[j]:
                            if random.random() > vaccine_efficacy:
                                initial_infected[j] = True
                            else:
                                vaccine_effective[j] = True
                        elif not vaccinated[j]:
                            if vaccination_started and random.random() < vaccination_rate:
                                vaccinated[j] = True
                                vaccine_effective[j] = True
                            else:
                                initial_infected[j] = True
                        new_infections += 1

        total_infected[round] = total_infected[round - 1] + new_infections

        # Introduce the vaccine at the specified round
        if round == vaccine_round:
            vaccination_started = True

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
num_social_connections = 10  # Number of social connections for each individual
social_ratio = 0.2  # Ratio of social connections contacted in each round
vaccine_round = 500  # Round at which the vaccine is introduced
vaccine_efficacy = 0.9  # Efficacy of the vaccine
vaccination_rate_low = 0.2  # Low vaccination rate
vaccination_rate_high = 0.8  # High vaccination rate

# Run the simulation for low vaccination rate
total_infected_low, R0_step6_low, R0_step7_low = simulate_pandemic(
    alpha, beta, t1, t2, T, num_social_connections, social_ratio, vaccine_round, vaccine_efficacy, vaccination_rate_low
)

# Run the simulation for high vaccination rate
total_infected_high, R0_step6_high, R0_step7_high = simulate_pandemic(
    alpha, beta, t1, t2, T, num_social_connections, social_ratio, vaccine_round, vaccine_efficacy, vaccination_rate_high
)

# Plot the results for low and high vaccination rates
plt.plot(range(T), total_infected_low, label=f'Low Vaccination Rate ({vaccination_rate_low})')
plt.plot(range(T), total_infected_high, label=f'High Vaccination Rate ({vaccination_rate_high})')

# Customize the plot
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread with Different Vaccination Rates')
plt.legend()
plt.show()

# Print R0 values for both scenarios
print(f'R0 for step 6 (Low Vaccination Rate): {R0_step6_low}')
print(f'R0 for step 7 (Low Vaccination Rate): {R0_step7_low}')
print(f'R0 for step 6 (High Vaccination Rate): {R0_step6_high}')
print(f'R0 for step 7 (High Vaccination Rate): {R0_step7_high}')
