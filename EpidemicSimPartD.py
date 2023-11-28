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

    # Lists to keep track of vaccination status
    vaccinated = [False] * N

    # Lists to store total infections for different vaccination rates
    total_infections = []

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(social_connections[i], int(social_ratio * num_social_connections))
                for j in contacts:
                    if not initial_infected[j] and random.random() < beta:
                        if not vaccinated[j]:
                            if random.random() < vaccination_rate:
                                vaccinated[j] = True
                            else:
                                initial_infected[j] = True
                        else:
                            if random.random() > vaccine_efficacy:
                                initial_infected[j] = True
                        new_infections += 1
        
        total_infected[round] = total_infected[round - 1] + new_infections

        # Introduce the vaccine at the specified round
        if round == vaccine_round:
            # Vaccinate individuals based on vaccination rate
            for i in range(N):
                if random.random() < vaccination_rate:
                    vaccinated[i] = True

        # Store the total infections for this round
        if round == T - 1:
            total_infections.append(total_infected[round])

    # Calculate R0 for step 6
    R0_step6 = total_infected[t1] / total_infected[0]

    # Calculate R0 for step 7
    R0_step7 = total_infected[t1 + t2] / total_infected[0]

    return total_infections, R0_step6, R0_step7

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

# Varying vaccination rates from 0 to 1
vaccination_rates = [i / 100 for i in range(101)]  # 0.00 to 1.00 in steps of 0.01

# Initialize a list to store total infections for each vaccination rate
total_infections = []

# Run simulations for different vaccination rates and record total infections
for vaccination_rate in vaccination_rates:
    total_infections_round, _, _ = simulate_pandemic(
        alpha, beta, t1, t2, T, num_social_connections, social_ratio, vaccine_round, vaccine_efficacy, vaccination_rate
    )
    total_infections.append(total_infections_round[0])  # Record total infections at the end

# Plot the total infections as a function of vaccination rate
plt.plot(vaccination_rates, total_infections)
plt.xlabel('Vaccination Rate')
plt.ylabel('Total Infections')
plt.title('Total Infections vs. Vaccination Rate')
plt.grid(True)
plt.show()
