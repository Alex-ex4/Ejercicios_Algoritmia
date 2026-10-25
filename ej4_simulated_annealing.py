import math
import random
import time
import matplotlib.pyplot as plt

def generate_cities(n=25, seed=100):
    rng = random.Random(seed)
    return [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(n)]

def tour_length(cities, route):
    return sum(
        math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
        for i in range(len(route))
    )

def simulated_annealing(cities, initial_route, schedule_type='exponential', T_init=100.0, T_min=1e-3, max_iter=5000):
    current = list(initial_route)
    current_cost = tour_length(cities, current)
    best = list(current)
    best_cost = current_cost

    history = [best_cost]
    n = len(cities)
    t_start = time.perf_counter()

    for step in range(1, max_iter + 1):
        if schedule_type == 'exponential':
            T = T_init * (0.995 ** step)
        elif schedule_type == 'linear':
            T = max(T_min, T_init * (1 - step / max_iter))
        elif schedule_type == 'logarithmic':
            T = T_init / (1 + math.log(1 + step))

        if T <= T_min:
            break

        #Movimiento 2-opt aleatorio
        i, k = sorted(random.sample(range(1, n), 2))
        neighbor = current[:i] + current[i:k + 1][::-1] + current[k + 1:]
        neighbor_cost = tour_length(cities, neighbor)

        delta = neighbor_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = list(current)
                best_cost = current_cost

        history.append(best_cost)

    elapsed_time = time.perf_counter() - t_start
    return best, best_cost, history, elapsed_time

if __name__ == '__main__':
    cities = generate_cities(n=25, seed=100)
    init_route = list(range(len(cities)))
    random.shuffle(init_route)

    schedules = ['exponential', 'linear', 'logarithmic']
    results = {}

    #Curvas de convergencia
    plt.figure(figsize=(10, 5))
    for sch in schedules:
        _, b_cost, hist, elapsed = simulated_annealing(cities, init_route, schedule_type=sch)
        results[sch] = (b_cost, elapsed)
        plt.plot(hist, label=f'Esquema: {sch.capitalize()} (Final: {b_cost:.1f})')

    plt.title('Curvas de Convergencia: Costo vs. Iteraciones (Simulated Annealing)')
    plt.xlabel('Iteraciones')
    plt.ylabel('Costo de la Mejor Ruta (Distancia)')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.tight_layout()
    plt.savefig('ej4_convergence.png')
    plt.show()

    #Comparativo de Tiempo vs. Calidad
    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax2 = ax1.twinx()

    names = [s.capitalize() for s in schedules]
    costs = [results[s][0] for s in schedules]
    times_list = [results[s][1] for s in schedules]

    x = range(len(names))
    ax1.bar([i - 0.15 for i in x], costs, width=0.3, color='tab:blue', align='center', label='Costo Final')
    ax2.bar([i + 0.15 for i in x], times_list, width=0.3, color='tab:orange', align='center', label='Tiempo Cómputo (s)')

    ax1.set_xticks(x)
    ax1.set_xticklabels(names)
    ax1.set_ylabel('Costo de la Solución Final', color='tab:blue')
    ax2.set_ylabel('Tiempo de Cómputo (s)', color='tab:orange')
    plt.title('Comparativo: Tiempo de Ejecución vs. Calidad de Solución')
    plt.tight_layout()
    plt.savefig('ej4_simulated_annealing.png')
    plt.show()