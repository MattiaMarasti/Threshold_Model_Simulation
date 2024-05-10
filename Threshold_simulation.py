import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
import pandas as pd

def calculate_threshold(G): #define a threshold for each node in the network
    threshold = [G.degree(i) * random.random() for i in G.nodes()]
    return threshold

def seed_set(G, m): #literally the initial conditions
    spin = np.zeros(len(G))
    seed = random.sample(list(G.nodes()), m)
    for i in seed:
        spin[i] = 1 
    return spin, seed

def threshold_model(G, steps, spin, threshold, seed): #this function carry out the simulation for a given network. 
    infected = [set(seed)]
    fraction_infected = np.zeros(steps + 1)
    fraction_infected[0] = len(seed) / len(G)
    for t in range(steps):
        newly_infected = set()
        for i in G.nodes():
            if spin[i] == 0 and sum(spin[j] for j in G.neighbors(i)) > threshold[i]:
                spin[i] = 1
                newly_infected.add(i)
        infected.append(newly_infected)
        fraction_infected[t + 1] = sum(len(inf) for inf in infected) / len(G)
    return fraction_infected

num_simulations = 5
steps = 20

# Two different networks to explore the role of topology in the process
G = nx.erdos_renyi_graph(1000, 0.2)
G1 = nx.barabasi_albert_graph(1000, 2)

# Plot for different simulations
fig, axs = plt.subplots(num_simulations, 2, figsize=(18, 5*num_simulations))

for sim in range(num_simulations):
    threshold = calculate_threshold(G)
    threshold_1 = calculate_threshold(G1)
    spin, seed = seed_set(G, 20)
    spin1, seed1 = seed_set(G1, 20)
    fraction_infected = threshold_model(G, steps, spin, threshold, seed)
    fraction_infected1 = threshold_model(G1, steps, spin1, threshold_1, seed1)
    
    # Plot the simulation on the Erdos Renyi graph
    axs[sim, 0].plot(range(steps + 1), fraction_infected, linewidth=3, color="red", label="Erdos Renyi")
    axs[sim, 0].set_ylabel("Contagiati")
    axs[sim, 0].set_xlabel("Tempo")
    axs[sim, 0].set_title(f"Simulazione {sim+1}")
    axs[sim, 0].legend()
    
    # Plot the simulation on the Albert Barabasi Graph
    axs[sim, 1].plot(range(steps + 1), fraction_infected1, linewidth=3, color="skyblue", label="Barabasi Albert")
    axs[sim, 1].set_ylabel("Contagiati")
    axs[sim, 1].set_xlabel("Tempo")
    axs[sim, 1].set_title(f"Simulazione {sim+1}")
    axs[sim, 1].legend()

plt.tight_layout()
plt.show()
