import numpy as np
import pandas as pd

# 定義城市的座標
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

# 提取城市名稱
city_names = list(cities.keys())
num_cities = len(city_names)

# 初始化距離矩陣
distance_matrix = np.zeros((num_cities, num_cities))

# 計算兩兩城市間的歐幾里得距離
for i, city1 in enumerate(city_names):
    for j, city2 in enumerate(city_names):
        if i != j:
            x1, y1 = cities[city1]
            x2, y2 = cities[city2]
            distance_matrix[i, j] = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

# 創建數據框並格式化數據
distance_df = pd.DataFrame(distance_matrix, index=city_names, columns=city_names).applymap(lambda x: f"{x:.2f}")

# 打印格式化的距離矩陣
print(distance_df)
