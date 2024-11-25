import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import permutations

# 定義城市及其座標
cities = {
    "A": (8, 3),
    "B": (50, 62),
    "C": (18, 0),
    "D": (35, 25),
    "E": (90, 89),
    "F": (40, 71),
    "G": (84, 7),
    "H": (74, 29),
    "I": (34, 45),
    "J": (40, 65),
    "K": (60, 69),
    "L": (74, 47)
}

city_names = list(cities.keys())  # 城市名稱列表
N = 10  # Bee數量
D = len(city_names) - 2  # 不固定首尾的城市數量
max_iter = 1000  # 最大迭代次數

# 計算兩城市之間的距離
def city_distance(city1, city2):
    x1, y1 = cities[city1]
    x2, y2 = cities[city2]
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# 計算總距離
def TtotalDistance(route):
    distance = sum(city_distance(route[i], route[i + 1]) for i in range(len(route) - 1))
    return distance

# 隨機產生初始食物源（路徑）
def foodsource(D):
    middle_cities = random.sample(city_names[1:-1], D)  # 隨機選擇中間的城市
    route = ["A"] + middle_cities + ["L"]  # 起點和終點固定
    return route

# Fitness函數
def fitness_machine(num):
    return 1 / (1 + num) if num >= 0 else 1 + abs(num)

# 產生初始食物源
food_source = [foodsource(D) for _ in range(N)]

# 計算初始距離和適應度
out_TD = [TtotalDistance(route) for route in food_source]
fitness_list = [fitness_machine(dist) for dist in out_TD]
trial = np.zeros(N).astype(int)

# 儲存歷史最佳解
everytime_best_route = []
everytime_best_distance = []

for it in range(max_iter):
    print(f"\n--- Iteration {it + 1} ---")
    
    # Employed Bee Phase
    print("Employed Bee Phase:")
    for i in range(N):
        current_route = food_source[i]
        new_route = current_route.copy()
        swap_indices = random.sample(range(1, D + 1), 2)  # 選擇兩個隨機交換的城市（不包括起點與終點）
        new_route[swap_indices[0]], new_route[swap_indices[1]] = (
            new_route[swap_indices[1]],
            new_route[swap_indices[0]],
        )
        new_distance = TtotalDistance(new_route)
        new_fitness = fitness_machine(new_distance)
        
        # 打印每個 bee 的更新過程
        print(f"  Bee {i + 1}: Current Route: {current_route}, Distance: {TtotalDistance(current_route)}, Fitness: {fitness_list[i]}")
        print(f"  Bee {i + 1}: New Route: {new_route}, Distance: {new_distance}, Fitness: {new_fitness}")
        
        if new_fitness > fitness_list[i]:  # 更新條件
            food_source[i] = new_route
            fitness_list[i] = new_fitness
            trial[i] = 0
            print(f"  Bee {i + 1}: Route updated.")
        else:
            trial[i] += 1
            print(f"  Bee {i + 1}: Route not updated.")

    # Onlooker Bee Phase
    print("\nOnlooker Bee Phase:")
    sum_fitness = sum(fitness_list)
    probabilities = [fitness / sum_fitness for fitness in fitness_list]
    for i in range(N):
        if random.random() < probabilities[i]:
            current_route = food_source[i]
            new_route = current_route.copy()
            swap_indices = random.sample(range(1, D + 1), 2)
            new_route[swap_indices[0]], new_route[swap_indices[1]] = (
                new_route[swap_indices[1]],
                new_route[swap_indices[0]],
            )
            new_distance = TtotalDistance(new_route)
            new_fitness = fitness_machine(new_distance)
            
            # 打印每個 bee 的選擇過程
            print(f"  Bee {i + 1}: Current Route: {current_route}, Distance: {TtotalDistance(current_route)}, Fitness: {fitness_list[i]}")
            print(f"  Bee {i + 1}: New Route: {new_route}, Distance: {new_distance}, Fitness: {new_fitness}")
            
            if new_fitness > fitness_list[i]:
                food_source[i] = new_route
                fitness_list[i] = new_fitness
                trial[i] = 0
                print(f"  Bee {i + 1}: Route updated.")
            else:
                trial[i] += 1
                print(f"  Bee {i + 1}: Route not updated.")
        else:
            print(f"  Bee {i + 1}: Skipped.")

    # Scout Bee Phase
    print("\nScout Bee Phase:")
    for i in range(N):
        if trial[i] > D:
            old_route = food_source[i]
            food_source[i] = foodsource(D)
            trial[i] = 0
            print(f"  Bee {i + 1}: Reinitialized Route: {old_route} -> {food_source[i]}")

    # 儲存最佳解
    best_index = np.argmax(fitness_list)
    best_route = food_source[best_index]
    best_distance = TtotalDistance(best_route)
    everytime_best_route.append(best_route)
    everytime_best_distance.append(best_distance)

    print(f"\nBest Route in Iteration {it + 1}: {best_route}")
    print(f"Best Distance in Iteration {it + 1}: {best_distance}")
    
    # 終止條件：只打印前兩次迭代
    if it == 1:
        break

# 打印最終最佳解
min_best_distance = min(everytime_best_distance)
best_index = everytime_best_distance.index(min_best_distance)
min_best_route = everytime_best_route[best_index]

print("\n--- Final Result ---")
print(f"Best Overall Route: {min_best_route}")
print(f"Best Overall Distance: {min_best_distance}")
