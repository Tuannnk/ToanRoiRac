import math

def min_players_per_map(n_players, n_maps):
    return math.ceil(n_players / n_maps)

n_players = int(input("Nhập số người chơi (n): "))
n_maps = int(input("Nhập số bản đồ (k): "))

min_per_map = min_players_per_map(n_players, n_maps)
print(f"Ít nhất 1 bản đồ có {min_per_map} người chơi.")

if min_per_map > 10:
    print("Cảnh báo: Cần tăng số lượng bản đồ!")