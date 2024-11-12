import random
import numpy as np

# 假設有 5 個城市，距離矩陣如下
dist_matrix = np.array([
    [0, 2, 9, 10, 7],
    [1, 0, 6, 4, 3],
    [15, 7, 0, 8, 9],
    [6, 3, 12, 0, 4],
    [8, 10, 9, 5, 0]
])

num_cities = len(dist_matrix)
num_bees = 10  # 蜂群數量
max_iterations = 100

# 計算路徑距離
def calculate_distance(path):
    return sum(dist_matrix[path[i], path[i + 1]] for i in range(len(path) - 1)) + dist_matrix[path[-1], path[0]]

# 隨機生成路徑
def random_path():
    path = list(range(num_cities))
    random.shuffle(path)
    return path

# ABC 算法
def abc_tsp():
    best_path = None
    best_distance = float('inf')

    # 初始化蜂群
    bees = [{'path': random_path(), 'distance': float('inf')} for _ in range(num_bees)]

    for _ in range(max_iterations):
        # 僱用蜂階段
        for bee in bees:
            bee['distance'] = calculate_distance(bee['path'])
            if bee['distance'] < best_distance:
                best_distance = bee['distance']
                best_path = bee['path']

        # 觀察蜂階段
        for bee in bees:
            new_path = bee['path'][:]
            i, j = random.sample(range(num_cities), 2)
            new_path[i], new_path[j] = new_path[j], new_path[i]
            new_distance = calculate_distance(new_path)
            if new_distance < bee['distance']:
                bee['path'], bee['distance'] = new_path, new_distance

        # 偵查蜂階段
        for bee in bees:
            if bee['distance'] >= best_distance:  # 假設當前路徑無法改善時成為偵查蜂
                bee['path'] = random_path()
                bee['distance'] = calculate_distance(bee['path'])

    return best_path, best_distance

# 執行算法
best_path, best_distance = abc_tsp()
print("最佳路徑:", best_path)
print("最短距離:", best_distance)
