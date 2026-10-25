import matplotlib.pyplot as plt

def greedy_knapsack_weight(values, weights, W):
    items = sorted(range(len(weights)), key=lambda i: weights[i])
    total_value, total_weight = 0, 0
    chosen = []
    for i in items:
        if total_weight + weights[i] <= W:
            chosen.append(i)
            total_weight += weights[i]
            total_value += values[i]
    return chosen, total_weight, total_value

def greedy_knapsack_ratio(values, weights, W):
    items = sorted(range(len(weights)), key=lambda i: values[i] / weights[i], reverse=True)
    total_value, total_weight = 0, 0
    chosen = []
    for i in items:
        if total_weight + weights[i] <= W:
            chosen.append(i)
            total_weight += weights[i]
            total_value += values[i]
    return chosen, total_weight, total_value

#Instancia para que el menor peso obtenga un resultado inferior
#Objeto 0: Peso 1, Valor 2  (Ratio 2.0)
#Objeto 1: Peso 10, Valor 100 (Ratio 10.0)
values = [2, 100]
weights = [1, 10]
W = 10

chosen_w, weight_w, val_w = greedy_knapsack_weight(values, weights, W)
chosen_r, weight_r, val_r = greedy_knapsack_ratio(values, weights, W)

print("=== Ejercicio 2: Instancia Diseñada ===")
print(f"Criterio 'Menor Peso': Objetos {chosen_w} | Capacidad Usada: {weight_w}/{W} | Valor Total: {val_w}")
print(f"Criterio 'Valor/Peso': Objetos {chosen_r} | Capacidad Usada: {weight_r}/{W} | Valor Total: {val_r}")

plt.figure(figsize=(7, 4.5))
methods = ['Menor Peso', 'Valor / Peso']
vals = [val_w, val_r]
colors = ['#e74c3c', '#2ecc71']

bars = plt.bar(methods, vals, color=colors, width=0.4)
plt.ylabel('Valor Total Obtenido')
plt.title('Comparación de Criterios Voraces para Mochila 0/1')
plt.ylim(0, 120)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f'Valor: {yval}', ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('ej2_greedy_knapsack.png')
plt.show()