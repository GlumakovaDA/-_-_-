import pulp

# медсестры по дням недели(количество из таблички)
r = [16, 15, 12, 14, 15, 18, 19]

model = pulp.LpProblem("Nurse_Scheduling", pulp.LpMinimize) #задача минимизации

x = [pulp.LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(7)]
#переменные, т.е.x[0] - сколько медсестер начинают работать в пн, x[1] - во вторник и тд.

# Целевая функция, 12000 * общее количество медсестер. минимизируем затраты.
model += 12000 * pulp.lpSum(x)

# какие медсестры рабоают в какой день
model += x[0] + x[3] + x[4] + x[5] + x[6] >= r[0]  # Пн
model += x[0] + x[1] + x[4] + x[5] + x[6] >= r[1]  # Вт
model += x[0] + x[1] + x[2] + x[5] + x[6] >= r[2]  # Ср
model += x[0] + x[1] + x[2] + x[3] + x[6] >= r[3]  # Чт
model += x[0] + x[1] + x[2] + x[3] + x[4] >= r[4]  # Пт
model += x[1] + x[2] + x[3] + x[4] + x[5] >= r[5]  # Сб
model += x[2] + x[3] + x[4] + x[5] + x[6] >= r[6]  # Вс

model.solve(pulp.PULP_CBC_CMD(msg=False))

print("\nОптимальное количество медсестёр (начало смены по дням):")
for i, var in enumerate(x):
    print(f"  {['Пн','Вт','Ср','Чт','Пт','Сб','Вс'][i]}: {var.varValue}")

total_nurses = sum(var.varValue for var in x)
print(f"\nОбщее число медсестёр: {total_nurses}")
print(f"Минимальные затраты: {12000 * total_nurses} руб.")