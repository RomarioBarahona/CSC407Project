import random
import matplotlib.pyplot as plt

# Step 1: Initialize the simulation
N = 1000  # Number of people
K = 10  # Number of communities
b = 20  # Number of bridge individuals
infected = [False] * N  # Array to record infection status
infected[0] = True  # Initial infected person
total_infected = [1]  # List to store the number of infected individuals after each round

# Parameters
alpha = 0.005  # Ratio of contacts within communities
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity

# Create community assignments for each individual
community_assignments = [random.randint(0, K - 1) for _ in range(N)]

# Step 2 to 4: Simulate the spread of the pandemic
T = 2000  # Total rounds
for round in range(1, T):
    new_infections = 1  # Initialize with 1 for the initial infected person
    for i in range(N):
        if infected[i]:
            contacts_within_community = [j for j in range(N) if community_assignments[j] == community_assignments[i]]
            contacts_outside_community = [j for j in range(N) if community_assignments[j] != community_assignments[i]]
            if i < b:
                contacts = random.sample(contacts_outside_community, int(alpha * len(contacts_outside_community)))
            else:
                contacts = random.sample(contacts_within_community, int(alpha * len(contacts_within_community)))

            for j in contacts:
                if not infected[j] and random.random() < beta:
                    infected[j] = True
                    new_infections += 1

    # Step 5: Record the number of infected individuals
    total_infected.append(total_infected[-1] + new_infections)

# Plot the results
plt.plot(range(T), total_infected)
plt.xlabel('Rounds')
plt.ylabel('Total Infected')
plt.title('Pandemic Spread in Communities')
plt.show()

# Step 6: Calculate R0 for step 6
R0_step6 = total_infected[t1] / total_infected[0]

# Step 7: Calculate R0 for step 7
R0_step7 = total_infected[t1 + t2] / total_infected[0]

print(f'R0 for step 6: {R0_step6}')
print(f'R0 for step 7: {R0_step7}')
