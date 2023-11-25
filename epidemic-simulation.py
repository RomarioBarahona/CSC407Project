import random
import matplotlib.pyplot as plt

# Step 1: Initialize the simulation
N = 1000  # Number of people
infected = [False] * N  # Array to record infection status
infected[0] = True  # Initial infected person
total_infected = [1]  # List to store the number of infected individuals after each round

# Parameters
alpha = 0.005  # Ratio of contacts
beta = 0.01  # Infection probability
t1 = 5  # Duration of infectiousness
t2 = 20  # Duration of immunity

# Step 2 to 4: Simulate the spread of the pandemic
T = 2000  # Total rounds
for round in range(1, T):
    new_infections = 0
    for i in range(N):
        if infected[i]:
            contacts = random.sample(range(N), int(alpha * N))
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
plt.title('Pandemic Spread')
plt.show()

# Step 6: Calculate R0 for step 6
R0_step6 = total_infected[t1] / total_infected[0]

# Step 7: Calculate R0 for step 7
R0_step7 = total_infected[t1 + t2] / total_infected[0]

print(f'R0 for step 6: {R0_step6}')
print(f'R0 for step 7: {R0_step7}')
