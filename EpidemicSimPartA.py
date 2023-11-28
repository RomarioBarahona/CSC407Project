import random
import matplotlib.pyplot as plt

# Function to simulate the pandemic spread in multiple communities with bridges
def simulate_pandemic_with_random_communities(alpha, beta, T):
    # Generate random values for the number of communities and their sizes
    num_communities = random.randint(10, 50)  # Random number of communities
    community_sizes = []
    remaining_people = 1000
    
    for _ in range(num_communities - 1):
        community_size = random.randint(1, remaining_people - (num_communities - len(community_sizes)) + 1)
        community_sizes.append(community_size)
        remaining_people -= community_size
    
    community_sizes.append(remaining_people)
    
    # Initialize the simulation
    N = sum(community_sizes)
    initial_infected = [False] * N
    total_infected = [0] * T

    # Divide people into communities
    communities = []
    start = 0
    for size in community_sizes:
        community = list(range(start, start + size))
        communities.append(community)
        start += size

    # Create random bridges between communities
    bridge_count = random.randint(1, 20)  # Random number of bridges
    for _ in range(bridge_count):
        community1, community2 = random.sample(range(num_communities), 2)
        person1 = random.choice(communities[community1])
        person2 = random.choice(communities[community2])
        # Connect the two individuals
        communities[community1].append(person2)
        communities[community2].append(person1)

    # Select a random initial infected person
    initial_infected_person = random.randint(0, N - 1)
    initial_infected[initial_infected_person] = True
    total_infected[0] = 1

    # Simulate the spread of the pandemic
    for round in range(1, T):
        new_infections = 0
        for i in range(N):
            if initial_infected[i]:
                community_index = next((index for index, community in enumerate(communities) if i in community), None)
                if community_index is not None:
                    contacts = random.sample(communities[community_index], int(alpha * N))
                    for j in contacts:
                        if not initial_infected[j] and random.random() < beta:
                            initial_infected[j] = True
                            new_infections += 1
        
        total_infected[round] = total_infected[round - 1] + new_infections

    return total_infected

# Parameters
alpha = 0.005     # Ratio of contacts
beta = 0.01       # Infection probability
T = 2000          # Total rounds

# Run the simulation for random communities with random sizes 5 times
for i in range(5):
    total_infected = simulate_pandemic_with_random_communities(alpha, beta, T)

    # Plot the results for each simulation
    plt.plot(range(T), total_infected, label=f'Simulation {i+1}')

# Customize the plot
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread in Random Communities with Bridges (5 Simulations)')
plt.legend()
plt.show()