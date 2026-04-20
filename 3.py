import numpy as np
from scipy.optimize import linprog

# затраты на 1 кг/л
c = [450, 50, 80, 100, 90, 120]  # говядина, картофель, молоко, апельсины, кефир, яблоки

# Матрица ограничений (A @ x >= b)
A = [
    [-250, -20, -30, -10, -30, -4],   # белки >= 50
    [0, -170, -50, -120, -40, -110],  # углеводы >= 150
    [-150, 0, -30, 0, -10, -1],       # жиры >= 40
    [0, 0, -0.5, -0.7, -0.2, -0.1],   # витамин А >= 0.7
    [0, -100, -10, -500, -5, -50],    # витамин С >= 60
    [-30, -5, -1, -1, -1, -2],        # железо >= 10
    [-50, -100, -1200, -400, -1200, -50]  # кальций >= 1000
]
b = [-50, -150, -40, -0.7, -60, -10, -1000]

bounds = [(0, None), (0, None), (0, None), (0, None), (0, None), (0, None)]

result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

print("\nОптимальный рацион (кг/л в сутки):")
print(f"  Говядина: {result.x[0]:.3f} кг")
print(f"  Картофель: {result.x[1]:.3f} кг")
print(f"  Молоко: {result.x[2]:.3f} л")
print(f"  Апельсины: {result.x[3]:.3f} кг")
print(f"  Кефир: {result.x[4]:.3f} л")
print(f"  Яблоки: {result.x[5]:.3f} кг")
print(f"\nМинимальные суточные затраты: {result.fun:.2f} руб.")

# Проверка выполнения норм
print("\nПроверка норм:")
print(f"Белки: {250*result.x[0] + 20*result.x[1] + 30*result.x[2] + 10*result.x[3] + 30*result.x[4] + 4*result.x[5]:.1f} г (≥50)")
print(f"Углеводы: {170*result.x[1] + 50*result.x[2] + 120*result.x[3] + 40*result.x[4] + 110*result.x[5]:.1f} г (≥150)")
print(f"Жиры: {150*result.x[0] + 30*result.x[2] + 10*result.x[4] + 1*result.x[5]:.1f} г (≥40)")
print(f"Витамин А: {0.5*result.x[2] + 0.7*result.x[3] + 0.2*result.x[4] + 0.1*result.x[5]:.2f} мг (≥0.7)")
print(f"Витамин С: {100*result.x[1] + 10*result.x[2] + 500*result.x[3] + 5*result.x[4] + 50*result.x[5]:.1f} мг (≥60)")
print(f"Железо: {30*result.x[0] + 5*result.x[1] + 1*result.x[2] + 1*result.x[3] + 1*result.x[4] + 2*result.x[5]:.1f} мг (≥10)")
print(f"Кальций: {50*result.x[0] + 100*result.x[1] + 1200*result.x[2] + 400*result.x[3] + 1200*result.x[4] + 50*result.x[5]:.1f} мг (≥1000)")