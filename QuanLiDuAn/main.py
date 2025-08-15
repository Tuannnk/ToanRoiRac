import csv
import math
import os
from itertools import permutations

# Lấy thư mục chứa file main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== Hàm đọc CSV và trả về danh sách =====
def read_csv_file(filename):
    file_path = os.path.join(BASE_DIR, filename)  # nối đường dẫn đầy đủ
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # bỏ dòng tiêu đề
        data = [row for row in reader]
    return data

# ===== Đọc file CSV =====
members = read_csv_file("members.csv")
tasks = read_csv_file("tasks.csv")
resources = read_csv_file("resources.csv")

# ===== 1. Tính số tổ hợp khi chọn m nhiệm vụ =====
def count_combinations(total_tasks, m):
    return math.comb(total_tasks, m)

# ===== 2. Tính số cách xếp lịch m nhiệm vụ vào n ngày =====
def count_schedules(m, n):
    return math.perm(m, n)

# ===== 3. Tính số phương án phân công mỗi nhiệm vụ cho 1 thành viên =====
def count_assignments(num_tasks, num_members):
    return num_members ** num_tasks

# ===== 4. Tính số phương án chọn 1 công nghệ trong nhiều loại =====
def count_tech_options(num_tech):
    return num_tech

# ======== DEMO CHẠY ========
total_tasks = len(tasks)
total_members = len(members)
total_resources = len(resources)

m = 3  # số nhiệm vụ chọn
n = 3  # số ngày sắp xếp

print("=== KẾT QUẢ TÍNH TOÁN ===")
print(f"1. Số tổ hợp chọn {m} nhiệm vụ: {count_combinations(total_tasks, m)}")
print(f"2. Số cách xếp lịch {m} nhiệm vụ vào {n} ngày: {count_schedules(m, n)}")
print(f"3. Số phương án phân công nhiệm vụ: {count_assignments(total_tasks, total_members)}")
print(f"4. Số phương án chọn công nghệ: {count_tech_options(total_resources)}")
