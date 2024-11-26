import matplotlib.pyplot as plt
import numpy as np
import random

# 城市座標
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

# 步驟1: 初始化蜜源（計算距離矩陣）
def create_distance_matrix(cities):
    city_names = list(cities.keys())
    num_cities = len(city_names)
    distance_matrix = np.zeros((num_cities, num_cities))
    for i, city1 in enumerate(city_names):
        for j, city2 in enumerate(city_names):
            if i != j:
                distance_matrix[i, j] = np.sqrt(
                    (cities[city1][0] - cities[city2][0])**2 + (cities[city1][1] - cities[city2][1])**2
                )
    return distance_matrix, city_names

# 計算路徑總距離
def calculate_total_distance(path, distance_matrix, city_names):
    total = 0
    for i in range(len(path) - 1):
        total += distance_matrix[city_names.index(path[i])][city_names.index(path[i + 1])]
    # 回到起點
    total += distance_matrix[city_names.index(path[-1])][city_names.index(path[0])]
    return total

# 步驟2: 雇傭蜂階段（局部搜索）
def employed_bee_phase(paths, distance_matrix, city_names):
    for i in range(len(paths)):
        current_path = paths[i]
        new_path = current_path[:]
        # 隨機交換兩個城市生成新路徑
        idx1, idx2 = random.sample(range(len(new_path)), 2)
        new_path[idx1], new_path[idx2] = new_path[idx2], new_path[idx1]
        # 更新蜜源（若新路徑更優）
        if calculate_total_distance(new_path, distance_matrix, city_names) < calculate_total_distance(current_path, distance_matrix, city_names):
            paths[i] = new_path
    return paths

# 步驟3: 觀察蜂階段（根據適應度選擇蜜源）
def onlooker_bee_phase(paths, distance_matrix, city_names, num_onlookers):
    fitness = [1 / calculate_total_distance(path, distance_matrix, city_names) for path in paths]
    probabilities = [f / sum(fitness) for f in fitness]
    onlooker_paths = []
    for _ in range(num_onlookers):
        selected_path = random.choices(paths, weights=probabilities, k=1)[0]
        onlooker_paths.append(selected_path)
    return onlooker_paths

# 步驟4: 偵查蜂階段（替換低效蜜源）
def scout_bee_phase(paths, distance_matrix, city_names, scout_threshold, stagnation_counts):
    for i in range(len(paths)):
        if stagnation_counts[i] > scout_threshold:  # 超過卡住次數限制
            print(f"Bee {i + 1} is stagnated. Reinitializing its path.")
            paths[i] = random.sample(city_names, len(city_names))  # 隨機替換蜜源
            stagnation_counts[i] = 0  # 重置卡住次數
    return paths

# 視覺化
def visualize_path(cities, path, title, total_distance=None):
    plt.figure(figsize=(8, 6))
    for city, coord in cities.items():
        plt.scatter(*coord, c='blue', zorder=2)
        plt.text(coord[0] + 1, coord[1], city, fontsize=8, zorder=2)

    for i in range(len(path)):
        start = cities[path[i]]
        end = cities[path[(i + 1) % len(path)]]
        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1], head_width=2, length_includes_head=True, color='red', alpha=0.7)

    if total_distance is not None:
        plt.title(f"{title}\nTotal Distance: {total_distance:.2f}")
    else:
        plt.title(title)
    plt.grid(True)
    plt.show()

# 蜂群演算法主程序
def bee_colony_tsp(cities, max_iterations=100, num_bees=30, scout_threshold=10):
    distance_matrix, city_names = create_distance_matrix(cities)

    # 初始化蜜蜂群體（隨機生成初始路徑）和卡住計數
    paths = [random.sample(city_names, len(city_names)) for _ in range(num_bees)]
    stagnation_counts = [0] * num_bees  # 每隻蜜蜂的卡住次數
    best_path = None
    best_distance = float("inf")
    iteration_distances = []  # 用於記錄每次迭代的最佳距離

    for iteration in range(max_iterations):
        print(f"Iteration {iteration + 1}/{max_iterations}")

        # 雇傭蜂階段
        old_paths = paths[:]
        paths = employed_bee_phase(paths, distance_matrix, city_names)
        for i in range(num_bees):
            # 如果路徑未更新，增加卡住計數
            if paths[i] == old_paths[i]:
                stagnation_counts[i] += 1
            else:
                stagnation_counts[i] = 0  # 路徑有更新，重置卡住計數

        # 觀察蜂階段
        paths = onlooker_bee_phase(paths, distance_matrix, city_names, num_bees)

        # 偵查蜂階段
        paths = scout_bee_phase(paths, distance_matrix, city_names, scout_threshold, stagnation_counts)

        # 更新最優解
        for path in paths:
            distance = calculate_total_distance(path, distance_matrix, city_names)
            if distance < best_distance:
                best_path = path
                best_distance = distance
                print(f"  New Best Path Found: {' -> '.join(best_path)} with Distance: {best_distance:.2f}")

        # 記錄當前最優距離
        iteration_distances.append(best_distance)

    # 繪製迭代過程中的最佳距離變化
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_iterations + 1), iteration_distances, marker='o', linestyle='-', color='b', label="Best Distance")
    
    # 標記最後一個數值
    final_iteration = max_iterations
    final_distance = iteration_distances[-1]
    plt.annotate(f"{final_distance:.2f}", 
                 (final_iteration, final_distance), 
                 textcoords="offset points", 
                 xytext=(-30, -10), 
                 ha='center', 
                 fontsize=10, 
                 color='red', 
                 arrowprops=dict(facecolor='red', arrowstyle='->'))
    
    # 添加標題和標籤
    plt.title("Best Distance vs Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Best Distance")
    plt.grid(True)
    plt.legend()
    plt.show()

    # 最終結果輸出
    print("\nFinal Best Path:")
    print(f"Best Path: {' -> '.join(best_path)}")
    print(f"Total Distance: {best_distance:.2f}")

    return best_path, best_distance



# 主程序執行
if __name__ == "__main__":
    best_path, best_distance = bee_colony_tsp(cities, max_iterations=800, num_bees=30, scout_threshold=30)
    print(f"Best Path: {' -> '.join(best_path)}")
    print(f"Total Distance: {best_distance:.2f}")
