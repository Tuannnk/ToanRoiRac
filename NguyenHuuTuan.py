import time

# 1. Đệ quy
def a_recursive(n):
    if n == 0:
        return 2
    return 3 * a_recursive(n - 1) - 4

# 2. Công thức nghiệm tổng quát (ở đây dãy hằng số = 2)
def a_formula(n):
    return 2

# ==============================
# Test với n = 30
n = 30

# Đệ quy
start = time.time()
val1 = a_recursive(n)
end = time.time()
print(f"Đệ quy: a_{n} = {val1}, thời gian: {end - start:.8f} s")

# Công thức
start = time.time()
val2 = a_formula(n)
end = time.time()
print(f"Công thức: a_{n} = {val2}, thời gian: {end - start:.8f} s")