import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread and calculate R0
def simulate_pandemic(alpha, beta, t1, t2, T, num_communities, bridges_per_community):
    # Initialize the simulation
    N = 1000  # Total number of people
    community_size = N // num_communities  # Size of each community
    initial_infected = [False] * N
    total_infected = [0] * T
    new_infections_per_round = [0] * T  # Store new infections per round

    # Create a list to track community membership for each individual
    community_membership = [i // community_size for i in range(N)]

    # Select a random initial infected person from a random community
    initial_infected_community = random.randint(0, num_communities - 1)
    initial_infected_person = random.randint(initial_infected_community * community_size, (initial_infected_community + 1) * community_size - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1
    new_infections_per_round[0] = 1

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                contacts = random.sample(range(N), int(alpha * N))
                for j in contacts:
                    # Check if i and j are in the same community or if j is a bridge
                    if (community_membership[i] == community_membership[j]) or (random.random() < bridges_per_community):
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
T = 2000  # Total rounds
num_communities = 10  # Number of communities
bridges_per_community = 0.1  # Fraction of people serving as bridges among communities

# Run the simulation 1 time
for i in range(1):
    total_infected, new_infections_per_round, R0_step6, R0_step7 = simulate_pandemic(alpha, beta, t1, t2, T, num_communities, bridges_per_community)

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
