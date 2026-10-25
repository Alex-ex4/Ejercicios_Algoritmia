import math
import random
import matplotlib.pyplot as plt

def generate_cities(n=20, seed=42):
    rng = random.Random(seed)
    return [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(n)]

def tour_length(cities, route):
    return sum(math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]]) for i in range(len(route)))

def nearest_neighbor_tour(cities, start_node):
    n = len(cities)
    unvisited = set(range(n))
    unvisited.remove(start_node)
    tour = [start_node]
    current = start_node
    while unvisited:
        nxt = min(unvisited, key=lambda c: math.dist(cities[current], cities[c]))
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    return tour

def two_opt_local_search(cities, initial_route):
    route = list(initial_route)
    n = len(route)
    improvements = 0
    improved = True
    while improved:
        improved = False
        best_cost = tour_length(cities, route)
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                # 2-opt swap
                new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
                new_cost = tour_length(cities, new_route)
                if new_cost < best_cost:
                    route = new_route
                    best_cost = new_cost
                    improvements += 1
                    improved = True
                    break
            if improved:
                break
    return route, best_cost, improvements

# Experimento con 50 ejecuciones
cities = generate_cities(n=25, seed=100)
num_trials = 50

random_improvements = []
random_costs = []
nn_improvements = []
nn_costs = []

for _ in range(num_trials):
    #Inicio aleatorio
    r_init = list(range(len(cities)))
    random.shuffle(r_init)
    _, r_cost, r_imp = two_opt_local_search(cities, r_init)
    random_improvements.append(r_imp)
    random_costs.append(r_cost)

    #Inicio con vecino más cercano
    start_node = random.randint(0, len(cities) - 1)
    nn_init = nearest_neighbor_tour(cities, start_node)
    _, nn_cost, nn_imp = two_opt_local_search(cities, nn_init)
    nn_improvements.append(nn_imp)
    nn_costs.append(nn_cost)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].boxplot([random_improvements, nn_improvements], tick_labels=['Aleatorio', 'Vecino Más Cercano'])
axes[0].set_title('Número de Mejoras 2-opt Necesarias')
axes[0].set_ylabel('Cantidad de Intercambios (Mejoras)')
axes[0].grid(True, linestyle='--', alpha=0.6)

axes[1].boxplot([random_costs, nn_costs], tick_labels=['Aleatorio', 'Vecino Más Cercano'])
axes[1].set_title('Calidad de Solución Alcanzada (Distancia)')
axes[1].set_ylabel('Costo del Óptimo Local')
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('ej3_2opt_tsp.png')
plt.show()