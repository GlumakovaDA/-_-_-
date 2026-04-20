import pulp
import pandas as pd

# табличка из презентации
data = {
    "school": list(range(1, 16)),
    "teachers": [40.2, 18.1, 42.5, 11.0, 24.8, 21.1, 13.5, 28.6, 23.5, 15.9, 23.2, 26.0, 11.1, 28.8, 19.7],
    "admin": [2.0, 1.1, 2.1, 0.8, 1.3, 1.3, 1.0, 1.3, 1.3, 1.0, 1.3, 1.4, 0.8, 1.6, 1.3],
    "computers": [37, 17, 41, 10, 22, 19, 13, 26, 22, 15, 22, 25, 11, 26, 18],
    "students": [760, 269, 648, 188, 420, 374, 247, 512, 411, 285, 397, 466, 198, 530, 357]
}

df = pd.DataFrame(data)

epsilon = 1e-4
results = []

for k in range(len(df)):
    model = pulp.LpProblem(f"DEA_School_{k + 1}", pulp.LpMaximize)

    u = pulp.LpVariable("u", lowBound=epsilon) #переменная, отвечающая за вес выхода(ученики)
    v1 = pulp.LpVariable("v1", lowBound=epsilon) #вес входа (учителя)
    v2 = pulp.LpVariable("v2", lowBound=epsilon) #вес входа (администрация)
    v3 = pulp.LpVariable("v3", lowBound=epsilon) #вес входа (компьютеры)

    # Целевая функция
    model += u * df.loc[k, "students"]

    # нормализация входов. теперь эффективность = u * y_k
    model += v1 * df.loc[k, "teachers"] + v2 * df.loc[k, "admin"] + v3 * df.loc[k, "computers"] == 1

    # Ограничения для всех школ: u * students[s] <= v1*teachers[s] + v2*admin[s] + v3*computers[s].
    # т.к. ни одна школа не может иметь эффективность > 1 при выбранных весах
    for s in range(len(df)):
        model += u * df.loc[s, "students"] <= v1 * df.loc[s, "teachers"] + v2 * df.loc[s, "admin"] + v3 * df.loc[
            s, "computers"]

    # Решение
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    efficiency = pulp.value(model.objective)
    # это u * y_k, но так как сумма входов = 1, это и есть эффективность
    results.append({
        "school": k + 1,
        "efficiency": efficiency,
        "status": pulp.LpStatus[model.status]
    })

print("Оценка эффективности школ")
print("-" * 50)
for r in results:
    if r["efficiency"] >= 0.9999:
        print(f"Школа {r['school']}: Эффективность = {r['efficiency']:.4f} -> эффективная")
    else:
        print(f"Школа {r['school']}: Эффективность = {r['efficiency']:.4f} -> неэффективная")
