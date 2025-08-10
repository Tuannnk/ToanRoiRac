a = 3 > 5
b = 4 != 4
print("a and b =", a and b)
print("a or b =", a or b)
print("a ^ b =", a ^ b)
print("not a =", not a)
# kq đầu ra 
# a and b = False
# a or b = False
# a ^ b = False
# not a = True
# giải thích
'''
a = 3 > 5: Phép so sánh 3 > 5 là sai, vì 3 không lớn hơn 5. Do đó, a = False.
b = 4 != 4: Phép so sánh 4 != 4 là sai, vì 4 bằng 4. Do đó, b = False.
a and b: False and False = False (cả hai đều sai, nên kết quả là False).
a or b: False or False = False (cả hai đều sai, nên không có giá trị nào là True).
a ^ b: False ^ False = False (XOR trả về True chỉ khi hai giá trị khác nhau, nhưng ở đây cả a và b đều là False, nên kết quả là False).
not a: not False = True (đảo ngược giá trị của a).
'''
#•	Thử thay a ^ b bằng a and (not b) và so sánh kết quả.
print("a and (not b) =", a and (not b))
# kq đầu ra
# a and (not b) = False
# giải thích 
'''
Toán tử ^ (XOR) trả về True khi hai giá trị khác nhau (True ^ False hoặc False ^ True).
Biểu thức a and (not b) chỉ trả về True nếu a = True và b = False (vì not False = True, nên True and True = True).
'''
# Dùng phép so sánh ==, !=, <, > trong một ví dụ tổng hợp để kết hợp với and, or.
x = 10
y = 5
z = 7

a = x > y  # 10 > 5
b = y != z  # 5 != 7
c = z < x  # 7 < 10
d = x == y + z  # 10 == 5 + 7

print("a (x > y) =", a)
print("b (y != z) =", b)
print("c (z < x) =", c)
print("d (x == y + z) =", d)
print("a and b =", a and b)
print("b or c =", b or c)
print("not d =", not d)
print("(a and b) or (c and not d) =", (a and b) or (c and not d))
# kq đầu ra
'''
a (x > y) = True
b (y != z) = True
c (z < x) = True
d (x == y + z) = False
a and b = True
b or c = True
not d = True
(a and b) or (c and not d) = True
'''
# giải thích
'''
a = x > y = 10 > 5 = True.
b = y != z = 5 != 7 = True.
c = z < x = 7 < 10 = True.
d = x == y + z = 10 == 5 + 7 = 10 == 12 = False.
a and b = True and True = True.
b or c = True or True = True.
not d = not False = True.
(a and b) or (c and not d) = (True and True) or (True and not False) = True or (True and True) = True or True = True.
'''