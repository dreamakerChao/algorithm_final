import matplotlib.pyplot as plt

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
# 指定路徑B -> F -> J -> I -> D -> A -> C -> G -> H -> L -> E -> K
path = ['B', 'F', 'J', 'I', 'D', 'A', 'C', 'G', 'H', 'L', 'E', 'K']
path2 = ['A', 'C', 'F', 'E', 'D', 'J', 'I', 'K', 'B', 'G', 'H', 'L']

# 繪製路徑
def plot_tsp_path(cities, path):
    plt.figure(figsize=(10, 8))

    # 繪製城市
    for city, coord in cities.items():
        plt.scatter(*coord, c='blue', zorder=2)
        plt.text(coord[0] + 1, coord[1], city, fontsize=10, zorder=3)
    
    # 繪製路徑
    '''for i in range(len(path)):
        start = cities[path[i]]
        end = cities[path[(i + 1) % len(path)]]  # 繞回起點
        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1],
                  head_width=1, length_includes_head=True, color='red', alpha=1, label="old")
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2'''


    for i in range(len(path)):
        start = cities[path[i]]
        end = cities[path[(i + 1) % len(path2)]]  # 繞回起點
        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1],
                  head_width=1, length_includes_head=True, color='red', alpha=1, label="new")
        

    # 圖表設置
    plt.title("TSP Path Visualization")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()

# 執行繪製
plot_tsp_path(cities, path)
