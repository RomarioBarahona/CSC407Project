import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, immune_duration):
    # Initialize the simulation
    N = 1000  # Number of people
    initial_infected = [False] * N
    total_infected = [0] * T
    new_infections_per_round = [0] * T  # Store new infections per round
    infections_caused_by_individual = [0] * N  # Store infections caused by each individual

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1
    new_infections_per_round[0] = 1

    # Initialize a list to track immunity duration for each individual
    immunity_duration = [0] * N

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(range(N), int(alpha * N))
                for j in contacts:
                    if random.random() < beta:
                        if not initial_infected[j] or immunity_duration[j] == 0:
                            initial_infected[j] = True
                            new_infections += 1
                            immunity_duration[j] = immune_duration  # Set immunity duration for the newly infected person
                            infections_caused_by_individual[i] += 1
        
        # Update immunity duration for each individual
        for i in range(N):
            if immunity_duration[i] > 0:
                immunity_duration[i] -= 1

        new_infections_per_round[round] = new_infections
        total_infected[round] = total_infected[round - 1] + new_infections

    # Calculate R0 for step 6
    R0_step6 = sum(infections_caused_by_individual[:t1]) / new_infections_per_round[0]

    # Calculate R0 for step 7
    R0_step7 = sum(infections_caused_by_individual[t1:(t1 + t2)]) / new_infections_per_round[0]

    return total_infected, new_infections_per_round, R0_step6, R0_step7

# Parameters
alpha = 0.005  # Ratio of contacts
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity
T = 2000  # Total rounds
immune_duration = 10  # Duration of immunity before individuals may be infected again

# Run the simulation 1 time
for i in range(1):
    total_infected, new_infections_per_round, R0_step6, R0_step7 = simulate_pandemic(alpha, beta, t1, t2, T, immune_duration)

    # Plot the results for total infected
    plt.figure(figsize=(10, 6))  # Create a new figure
    plt.subplot(2, 1, 1)  # Create the first subplot
    plt.plot(range(T), total_infected, label='Total Infected')
    plt.ylabel('Total Infected')
    plt.title('Total Infected Individuals')

    # Plot the results for new infections per round
    plt.subplot(2, 1, 2)  # Create the second subplot
    plt.plot(range(T), new_infections_per_round, label='New Infections per Round')
    plt.xlabel('Rounds')
    plt.ylabel('New Infections per Round')
    plt.title('New Infections per Round')

    plt.tight_layout()  # Ensure proper spacing between subplots

# Show the plots
plt.show()

# Print R0 values for the last simulation
print(f'R0 for step 6 (last simulation): {R0_step6}')
print(f'R0 for step 7 (last simulation): {R0_step7}')
