# Thêm điều kiện elif nhiet_do < 50: → xử lý "Nước lạnh".
# Viết lại hàm bằng cú pháp ngắn gọn return "..." if ... else "...".
def kiemtra_nuocsoi(nhiet_do):
    if nhiet_do < 50:
        return "Nước lạnh"
    elif nhiet_do < 100:
        return "Nước chưa sôi"
    else:
        return "Nước đã sôi"

print(kiemtra_nuocsoi(99))
print(kiemtra_nuocsoi(100))
# Kiểm tra hàm với giá trị âm (-10) và giải thích logic hoạt động.
print(kiemtra_nuocsoi(-10))
# kq
'''
Nước chưa sôi
Nước đã sôi
Nước lạnh
'''
# giải thích
'''
Thêm điều kiện if nhiet_do < 50 với kết quả "Nước lạnh".
elif nhiet_do < 100 giờ chỉ áp dụng cho các giá trị từ 50 đến 99, trả về "Nước chưa sôi".
else vẫn áp dụng cho nhiet_do >= 100, trả về "Nước đã sôi".
Vì -10 < 50, chương trình vào nhánh if đầu tiên và trả về "Nước lạnh".
'''