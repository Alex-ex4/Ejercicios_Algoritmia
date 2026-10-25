import multiprocessing as mp
import time
import random
import matplotlib.pyplot as plt

def estimate_pi(seed: int, samples: int = 10_000_000) -> float:
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

if __name__ == '__main__':
    process_counts = [1, 2, 4, 8]
    num_seeds = 16 
    times = []

    print("=== Ejercicio 1: Experimento de Speedup Paralelo ===")
    for p in process_counts:
        seeds = list(range(num_seeds))
        t0 = time.perf_counter()
        with mp.Pool(processes=p) as pool:
            results = pool.map(estimate_pi, seeds)
        t_elapsed = time.perf_counter() - t0
        times.append(t_elapsed)
        print(f"Procesos: {p:>2} | Tiempo: {t_elapsed:.4f} s | Pi estimado: {sum(results)/len(results):.5f}")

    t1 = times[0]
    speedups = [t1 / tp for tp in times]
    ideal_speedups = process_counts

    plt.figure(figsize=(8, 5))
    plt.plot(process_counts, speedups, 'o-', linewidth=2, label='Speedup Real (Obtenido)')
    plt.plot(process_counts, ideal_speedups, 'k--', linewidth=2, label='Speedup Ideal (Lineal)')
    plt.title('Parallel Speedup - Monte Carlo Pi')
    plt.xlabel('Número de Procesos (Núcleos)')
    plt.ylabel('Aceleración (Speedup $S_p = T_1 / T_p$)')
    plt.xticks(process_counts)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('ej1_parallel_speedup.png')
    plt.show()