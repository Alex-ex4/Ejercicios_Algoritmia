import itertools
import math
import random
import matplotlib.pyplot as plt

# ==========================================
# 1. FUNCIONES BASE Y DE UTILIDAD
# ==========================================

def tour_length(cities, route):
    return sum(
        math.dist(cities[route[i]], cities[route[(i + 1) % len(route)]])
        for i in range(len(route))
    )

def two_opt_local_search(cities, initial_route):
    route = list(initial_route)
    n = len(route)
    improved = True
    
    while improved:
        improved = False
        best_cost = tour_length(cities, route)
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                new_route = route[:i] + route[i:k + 1][::-1] + route[k + 1:]
                new_cost = tour_length(cities, new_route)
                if new_cost < best_cost:
                    route = new_route
                    best_cost = new_cost
                    improved = True
                    break
            if improved:
                break
    return route, best_cost, 0

def simulated_annealing(cities, initial_route, T_init=100.0, T_min=1e-3, max_iter=1000):
    current = list(initial_route)
    current_cost = tour_length(cities, current)
    best = list(current)
    best_cost = current_cost
    n = len(cities)

    for step in range(1, max_iter + 1):
        T = T_init * (0.995 ** step)
        if T <= T_min:
            break

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

    return best, best_cost, None, None

def mst_prim(points):
    n = len(points)
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, n)}
    children = {v: [] for v in range(n)}
    while best:
        v = min(best, key=lambda u: best[u][0])
        children[best.pop(v)[1]].append(v)
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
    return children

def preorder(children, root=0):
    return [root] + [c for child in children[root] for c in preorder(children, child)]

def brute_force_optimal(points):
    n = len(points)
    return min(
        ((0,) + p for p in itertools.permutations(range(1, n))),
        key=lambda t: tour_length(points, t)
    )

if __name__ == '__main__':
    random.seed(42)
    num_instances = 100
    
    ratios = []
    costs_mst = []
    costs_mst_2opt = []
    costs_hc = []
    costs_sa = []

    print(f"Ejecutando experimento en {num_instances} instancias aleatorias de 9 ciudades...")

    for seed in range(num_instances):
        #Generar 9 ciudades aleatorias en un plano 100x100
        rng = random.Random(seed)
        pts = [(rng.uniform(0, 100), rng.uniform(0, 100)) for _ in range(9)]
        
        #Fuerza bruta
        opt_tour = brute_force_optimal(pts)
        opt_cost = tour_length(pts, opt_tour)
        
        #MST
        mst_tour = preorder(mst_prim(pts))
        mst_cost = tour_length(pts, mst_tour)
        
        #MST + post-procesamiento 2-opt
        _, mst_2opt_cost, _ = two_opt_local_search(pts, mst_tour)
        
        #Búsqueda Local
        init_r = list(range(9))
        random.shuffle(init_r)
        _, hc_cost, _ = two_opt_local_search(pts, init_r)
        
        #Recocido Simulado
        _, sa_cost, _, _ = simulated_annealing(pts, init_r)
        
        ratios.append(mst_cost / opt_cost)
        costs_mst.append(mst_cost)
        costs_mst_2opt.append(mst_2opt_cost)
        costs_hc.append(hc_cost)
        costs_sa.append(sa_cost)

    print("Experimento completado. Generando gráficas...")

    #Histograma de la razón de aproximación
    plt.figure(figsize=(8, 4.5))
    plt.hist(ratios, bins=15, color='#3498db', edgecolor='black', alpha=0.7)
    plt.axvline(2.0, color='red', linestyle='--', linewidth=2, label='Límite Teórico Garantizado (2.0)')
    plt.title('Distribución de la Razón de Aproximación ($C_{obtenido} / C_{óptimo}$)')
    plt.xlabel('Razón de Aproximación')
    plt.ylabel('Frecuencia (100 Instancias)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('ej5_approximation_ratio.png')
    plt.show()

    #Boxplot comparativo entre métodos
    plt.figure(figsize=(9, 5))
    plt.boxplot(
        [costs_mst, costs_mst_2opt, costs_hc, costs_sa],
        tick_labels=['MST Puro', 'MST + 2-opt', 'Hill Climbing', 'Simulated Annealing']
    )
    plt.title('Comparación de Calidad de Solución entre Métodos (100 Instancias)')
    plt.ylabel('Costo del Recorrido (Distancia Total)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('ej5_mst_aproximation.png')
    plt.show()