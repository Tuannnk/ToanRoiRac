import json
import re

danh_sach_sinh_vien = []
ti_chi_hoc_bong = {
    "muc_1": {"diem_hoc_luc": 9.0, "diem_ren_luyen": 90, "so_tien": 5000000},
    "muc_2": {"diem_hoc_luc": 8.5, "diem_ren_luyen": 85, "so_tien": 3000000},
    "muc_3": {"diem_hoc_luc": 8.0, "diem_ren_luyen": 80, "so_tien": 1500000}
}

def doc_file():
    """Đọc dữ liệu sinh viên từ file students.json"""
    global danh_sach_sinh_vien
    try:
        with open("students.json", "r", encoding="utf-8") as file:
            danh_sach_sinh_vien = json.load(file)
    except FileNotFoundError:
        print("File students.json không tồn tại, sẽ tạo file mới khi ghi dữ liệu.")
        danh_sach_sinh_vien = []
    except json.JSONDecodeError:
        print("Dữ liệu trong file JSON không hợp lệ!")
        danh_sach_sinh_vien = []
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        danh_sach_sinh_vien = []

def ghi_file():
    """Ghi dữ liệu sinh viên vào file students.json"""
    try:
            with open("students.json", "w", encoding="utf-8") as file:
                json.dump(danh_sach_sinh_vien, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Lỗi khi ghi file: {e}")

def kiem_tra_ma_sv(ma_sv):
    """Kiểm tra định dạng mã sinh viên (SV + 3 số)"""
    pattern = r"^SV\d{3}$"
    return bool(re.match(pattern, ma_sv))

def them_sv():
    """Thêm sinh viên mới vào danh sách"""
    ma_sv = input("Nhập mã sinh viên (SV + 3 số, ví dụ: SV001): ")
    if not kiem_tra_ma_sv(ma_sv):
        print("Mã sinh viên không hợp lệ! Phải có định dạng SV + 3 số (VD: SV001).")
        return
    for sv in danh_sach_sinh_vien:
        if sv["ma"] == ma_sv:
            print("Mã sinh viên đã tồn tại!")
            return
    ho_ten = input("Nhập hệ tên sinh viên: ")
    sinh_vien = {"ma": ma_sv, "ho_ten": ho_ten, "hoc_ky_1": {}, "hoc_ky_2": {}, "hoc_ky_3": {}}
    for ky in ["hoc_ky_1", "hoc_ky_2", "hoc_ky_3"]:
        try:
            print(f"Nhập điểm cho {ky.replace('_', ' ').title()}:")
            diem_hoc_luc = float(input("Nhập điểm học lực (0-10): "))
            diem_ren_luyen = float(input("Nhập điểm rèn luyện (0-100): "))
            if 0 <= diem_hoc_luc <= 10 and 0 <= diem_ren_luyen <= 100:
                sinh_vien[ky] = {"diem_hoc_luc": diem_hoc_luc, "diem_ren_luyen": diem_ren_luyen}
            else:
                print("Điểm học lực hoặc điểm rèn luyện không hợp lệ!")
                return
        except ValueError:
            print("Vui lòng nhập số hợp lệ cho điểm!")
            return
    danh_sach_sinh_vien.append(sinh_vien)
    ghi_file()
    print("Thêm sinh viên thành công!")

def hien_thi():
    """Hiển thị danh sách sinh viên"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    print("\nDanh sách sinh viên:")
    print("Mã SV\tHọ tên\t\tKỳ 1 HL\tKỳ 1 RL\tKỳ 2 HL\tKỳ 2 RL\tKỳ 3 HL\tKỳ 3 RL")
    for sv in danh_sach_sinh_vien:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_1']['diem_hoc_luc']}\t{sv['hoc_ky_1']['diem_ren_luyen']}\t"
            f"{sv['hoc_ky_ky2']['diem_hoc_luc']}\t{sv['hoc_ky_2']['diem_ren_luyen']}\t"
            f"{sv['hoc_ky_3']['diem_hoc_luc']}\t{sv['hoc_ky_3']['diem_ren_luyen']}")

def cap_nhat_thong_tin():
    """Cập nhật thông tin sinh viên"""
    ma_sv = input("Nhập mã sinh viên cần cập nhật: ")
    for sv in danh_sach_sinh_vien:
        if sv["ma"] == ma_sv:
            print("Nhập thông tin mới (nhấn Enter để giữ nguyên):")
            ho_ten = input(f"Họ tên ({sv['ho_ten']}): ") or sv["ho_ten"]
            sv["ho_ten"] = ho_ten
            for ky in ["hoc_ky_1", "hoc_ky_2", "hoc_ky_3"]:
                print(f"Cập nhật {ky.replace('_', ' ').title()}:")
                try:
                    diem_hoc_luc = input(f"Điểm học lực ({sv[ky]['diem_hoc_luc']}): ")
                    diem_hoc_luc = float(diem_hoc_luc) if diem_hoc_luc else sv[ky]["diem_hoc_luc"]
                    diem_ren_luyen = input(f"Điểm rèn luyện ({sv[ky]['diem_ren_luyen']}): ")
                    diem_ren_luyen = float(diem_ren_luyen) if diem_ren_luyen else sv[ky]["diem_ren_luyen"]
                    if 0 <= diem_hoc_luc <= 10 and 0 <= diem_ren_luyen <= 100:
                        sv[ky] = {"diem_hoc_luc": diem_hoc_luc, "diem_ren_luyen": diem_ren_luyen}
                    else:
                        print("Điểm học lực hoặc điểm rèn luyện không hợp lệ!")
                        return
                except ValueError:
                    print("Vui lòng nhập số hợp lệ cho điểm!")
                    return
            ghi_file()
            print("Cập nhật thông tin thành công!")
            return
    print("Không tìm thấy sinh viên với mã này!")

def xoa_sinh_vien():
    """Xóa sinh viên khỏi danh sách"""
    ma_sv = input("Nhập mã sinh viên cần xóa: ")
    for i, sv in enumerate(danh_sach_sinh_vien):
        if sv["ma"] == ma_sv:
            danh_sach_sinh_vien.pop(i)
            ghi_file()
            print("Xóa sinh viên thành công!")
            return
    print("Không tìm thấy sinh viên với mã này!")

def xet_hoc_bong(diem_hoc_luc, diem_ren_luyen):
    """Xét điều kiện và mức học bổng"""
    for muc in ti_chi_hoc_bong.values():
        if diem_hoc_luc >= muc["diem_hoc_luc"] and diem_ren_luyen >= muc["diem_ren_luyen"]:
            return True, muc["so_tien"]
    return False, 0

def thong_ke_hoc_bong_ky(ky):
    """Thống kê và xét học bổng cho học kỳ cụ thể"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    print(f"\nThống kê học bổng {ky.replace('_', ' ').title()}:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện\tHọc bổng\tMức hỗ trợ")
    tong_tien = 0
    so_sv_duoc_hoc_bong = 0
    for sv in danh_sach_sinh_vien:
        co_hoc_bong, so_tien = xet_hoc_bong(sv[ky]["diem_hoc_luc"], sv[ky]["diem_ren_luyen"])
        trang_thai = "Có" if co_hoc_bong else "Không"
        if co_hoc_bong:
            so_sv_duoc_hoc_bong += 1
            tong_tien += so_tien
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv[ky]['diem_hoc_luc']}\t\t{sv[ky]['diem_ren_luyen']}\t\t{trang_thai}\t\t{so_tien:,} VNĐ")
    print(f"\nTổng số sinh viên nhận học bổng: {so_sv_duoc_hoc_bong}")
    print(f"Tổng số tiền học bổng: {tong_tien:,} VNĐ")

def tim_kiem_sinh_vien():
    """Tìm kiếm sinh viên theo mã hoặc tên"""
    tu_khoa = input("Nhập mã sinh viên hoặc tên sinh viên cần tìm: ").lower().strip()
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if tu_khoa in sv["ma"].lower() or tu_khoa in sv["ho_ten"].lower():
            ket_qua.append(sv)
    if not ket_qua:
        print("Không tìm thấy sinh viên nào phù hợp!")
        return
    print("\nKết quả tìm kiếm:")
    print("Mã SV\tHọ tên\t\tKỳ 1 HL\tKỳ 1 RL\tKỳ 2 HL\tKỳ 2 RL\tKỳ 3 HL\tKỳ 3 RL")
    for sv in ket_qua:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_1']['diem_hoc_luc']}\t{sv['hoc_ky_1']['diem_ren_luyen']}\t"
              f"{sv['hoc_ky_2']['diem_hoc_luc']}\t{sv['hoc_ky_2']['diem_ren_luyen']}\t"
              f"{sv['hoc_ky_3']['diem_hoc_luc']}\t{sv['hoc_ky_3']['diem_ren_luyen']}")

def sap_xep_theo_diem_hoc_luc_ky2():
    """Sắp xếp theo điểm học lực kỳ 2 từ cao đến thấp"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    danh_sach_sinh_vien.sort(key=lambda x: x["hoc_ky_2"]["diem_hoc_luc"], reverse=True)
    print("Đã sắp xếp theo điểm học lực kỳ 2 từ cao đến thấp!")
    hien_thi()

def liet_ke_gpa_8_ky3():
    """Liệt kê sinh viên có GPA >= 8 kỳ 3"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if sv["hoc_ky_3"]["diem_hoc_luc"] >= 8.0:
            ket_qua.append(sv)
    if not ket_qua:
        print("Không có sinh viên nào có GPA >= 8 kỳ 3!")
        return
    print("\nSinh viên có GPA >= 8 kỳ 3:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện")
    for sv in ket_qua:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_3']['diem_hoc_luc']}\t\t{sv['hoc_ky_3']['diem_ren_luyen']}")

def sap_xep_theo_diem_ren_luyen_ky1():
    """Sắp xếp theo điểm rèn luyện kỳ 1 từ cao đến thấp"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    danh_sach_sinh_vien.sort(key=lambda x: x["hoc_ky_1"]["diem_ren_luyen"], reverse=True)
    print("Đã sắp xếp theo điểm rèn luyện kỳ 1 từ cao đến thấp!")
    hien_thi()

def liet_ke_diem_ren_luyen_80_ky2():
    """Liệt kê sinh viên có điểm rèn luyện >= 80 kỳ 2"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if sv["hoc_ky_2"]["diem_ren_luyen"] >= 80:
            ket_qua.append(sv)
    if not ket_qua:
        print("Không có sinh viên nào có điểm rèn luyện >= 80 kỳ 2!")
        return
    print("\nSinh viên có điểm rèn luyện >= 80 kỳ 2:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện")
    for sv in ket_qua:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_2']['diem_hoc_luc']}\t\t{sv['hoc_ky_2']['diem_ren_luyen']}")

def sap_xep_theo_ten():
    """Sắp xếp theo tên"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    danh_sach_sinh_vien.sort(key=lambda x: x["ho_ten"].lower())
    print("Đã sắp xếp theo tên!")
    hien_thi()

def liet_ke_co_hoc_bong_ky3():
    """Liệt kê sinh viên có học bổng kỳ 3"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if xet_hoc_bong(sv["hoc_ky_3"]["diem_hoc_luc"], sv["hoc_ky_3"]["diem_ren_luyen"])[0]:
            ket_qua.append(sv)
    if not ket_qua:
        print("Không có sinh viên nào có học bổng kỳ 3!")
        return
    print("\nSinh viên có học bổng kỳ 3:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện\tMức hỗ trợ")
    for sv in ket_qua:
        _, so_tien = xet_hoc_bong(sv["hoc_ky_3"]["diem_hoc_luc"], sv["hoc_ky_3"]["diem_ren_luyen"])
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_3']['diem_hoc_luc']}\t\t{sv['hoc_ky_3']['diem_ren_luyen']}\t\t{so_tien:,} VNĐ")

def liet_ke_khong_co_hoc_bong_ky1():
    """Liệt kê sinh viên không có học bổng kỳ 1"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if not xet_hoc_bong(sv["hoc_ky_1"]["diem_hoc_luc"], sv["hoc_ky_1"]["diem_ren_luyen"])[0]:
            ket_qua.append(sv)
    if not ket_qua:
        print("Tất cả sinh viên đều có học bổng kỳ 1!")
        return
    print("\nSinh viên không có học bổng kỳ 1:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện")
    for sv in ket_qua:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_1']['diem_hoc_luc']}\t\t{sv['hoc_ky_1']['diem_ren_luyen']}")

def thong_ke_muc_hoc_bong_ky2():
    """Thống kê số lượng sinh viên theo mức học bổng kỳ 2"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    dem = {"muc_1": 0, "muc_2": 0, "muc_3": 0, "khong": 0}
    for sv in danh_sach_sinh_vien:
        co_hoc_bong, so_tien = xet_hoc_bong(sv["hoc_ky_2"]["diem_hoc_luc"], sv["hoc_ky_2"]["diem_ren_luyen"])
        if not co_hoc_bong:
            dem["khong"] += 1
        elif so_tien == ti_chi_hoc_bong["muc_1"]["so_tien"]:
            dem["muc_1"] += 1
        elif so_tien == ti_chi_hoc_bong["muc_2"]["so_tien"]:
            dem["muc_2"] += 1
        else:
            dem["muc_3"] += 1
    print("\nThống kê số lượng sinh viên theo mức học bổng kỳ 2:")
    print(f"Mức 5,000,000 VNĐ: {dem['muc_1']} sinh viên")
    print(f"Mức 3,000,000 VNĐ: {dem['muc_2']} sinh viên")
    print(f"Mức 1,500,000 VNĐ: {dem['muc_3']} sinh viên")
    print(f"Không có học bổng: {dem['khong']} sinh viên")

def liet_ke_theo_khoang_diem_hoc_luc_ky3():
    """Liệt kê sinh viên theo khoảng điểm học lực kỳ 3"""
    try:
        min_diem = float(input("Nhập điểm học lực tối thiểu (0-10): "))
        max_diem = float(input("Nhập điểm học lực tối đa (0-10): "))
        if not (0 <= min_diem <= 10 and 0 <= max_diem <= 10 and min_diem <= max_diem):
            print("Khoảng điểm không hợp lệ!")
            return
        ket_qua = []
        for sv in danh_sach_sinh_vien:
            if min_diem <= sv["hoc_ky_3"]["diem_hoc_luc"] <= max_diem:
                ket_qua.append(sv)
        if not ket_qua:
            print("Không tìm thấy sinh viên trong khoảng điểm này!")
            return
        print(f"\nSinh viên có điểm học lực kỳ 3 từ {min_diem} đến {max_diem}:")
        print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện")
        for sv in ket_qua:
            print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_3']['diem_hoc_luc']}\t\t{sv['hoc_ky_3']['diem_ren_luyen']}")
    except ValueError:
        print("Vui lòng nhập số hợp lệ cho điểm!")

def liet_ke_theo_khoang_diem_ren_luyen_ky1():
    """Liệt kê sinh viên theo khoảng điểm rèn luyện kỳ 1"""
    try:
        min_diem = float(input("Nhập điểm rèn luyện tối thiểu (0-100): "))
        max_diem = float(input("Nhập điểm rèn luyện tối đa (0-100): "))
        if not (0 <= min_diem <= 100 and 0 <= max_diem <= 100 and min_diem <= max_diem):
            print("Khoảng điểm không hợp lệ!")
            return
        ket_qua = []
        for sv in danh_sach_sinh_vien:
            if min_diem <= sv["hoc_ky_1"]["diem_ren_luyen"] <= max_diem:
                ket_qua.append(sv)
        if not ket_qua:
            print("Không tìm thấy sinh viên trong khoảng điểm này!")
            return
        print(f"\nSinh viên có điểm rèn luyện kỳ 1 từ {min_diem} đến {max_diem}:")
        print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện")
        for sv in ket_qua:
            print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_1']['diem_hoc_luc']}\t\t{sv['hoc_ky_1']['diem_ren_luyen']}")
    except ValueError:
        print("Vui lòng nhập số hợp lệ cho điểm!")

def cap_nhat_ti_chi_hoc_bong():
    """Cập nhật tiêu chí học bổng"""
    global ti_chi_hoc_bong
    print("Các mức học bổng hiện tại:")
    for muc, chi_tiet in ti_chi_hoc_bong.items():
        print(f"{muc}: Điểm học lực >= {chi_tiet['diem_hoc_luc']}, Điểm rèn luyện >= {chi_tiet['diem_ren_luyen']}, Số tiền: {chi_tiet['so_tien']:,} VNĐ")
    muc = input("Nhập mức muốn cập nhật (muc_1, muc_2, muc_3): ")
    if muc not in ti_chi_hoc_bong:
        print("Mức học bổng không hợp lệ!")
        return
    try:
        diem_hoc_luc = input(f"Nhập điểm học lực tối thiểu mới (hiện tại: {ti_chi_hoc_bong[muc]['diem_hoc_luc']}): ")
        diem_hoc_luc = float(diem_hoc_luc) if diem_hoc_luc else ti_chi_hoc_bong[muc]["diem_hoc_luc"]
        diem_ren_luyen = input(f"Nhập điểm rèn luyện tối thiểu mới (hiện tại: {ti_chi_hoc_bong[muc]['diem_ren_luyen']}): ")
        diem_ren_luyen = float(diem_ren_luyen) if diem_ren_luyen else ti_chi_hoc_bong[muc]["diem_ren_luyen"]
        so_tien = input(f"Nhập số tiền học bổng mới (hiện tại: {ti_chi_hoc_bong[muc]['so_tien']:,} VNĐ): ")
        so_tien = int(so_tien) if so_tien else ti_chi_hoc_bong[muc]["so_tien"]
        if 0 <= diem_hoc_luc <= 10 and 0 <= diem_ren_luyen <= 100 and so_tien >= 0:
            ti_chi_hoc_bong[muc] = {"diem_hoc_luc": diem_hoc_luc, "diem_ren_luyen": diem_ren_luyen, "so_tien": so_tien}
            print("Cập nhật tiêu chí học bổng thành công!")
        else:
            print("Dữ liệu nhập không hợp lệ!")
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")

def hien_thi_ti_chi_hoc_bong():
    """Hiển thị tiêu chí học bổng"""
    print("\nTiêu chí học bổng hiện tại:")
    print("Mức\tĐiểm học lực\tĐiểm rèn luyện\tSố tiền")
    for muc, chi_tiet in ti_chi_hoc_bong.items():
        print(f"{muc}\t{chi_tiet['diem_hoc_luc']}\t\t{chi_tiet['diem_ren_luyen']}\t\t{chi_tiet['so_tien']:,} VNĐ")

def liet_ke_hoc_bong_tren_muc_ky(ky, muc_tien):
    """Liệt kê sinh viên có học bổng trên mức tiền cho học kỳ cụ thể"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        if xet_hoc_bong(sv[ky]["diem_hoc_luc"], sv[ky]["diem_ren_luyen"])[1] > muc_tien:
            ket_qua.append(sv)
    if not ket_qua:
        print(f"Không có sinh viên nào có học bổng trên {muc_tien:,} VNĐ ở {ky.replace('_', ' ').title()}!")
        return
    print(f"\nSinh viên có học bổng trên {muc_tien:,} VNĐ ở {ky.replace('_', ' ').title()}:")
    print("Mã SV\tHọ tên\t\tĐiểm học lực\tĐiểm rèn luyện\tMức hỗ trợ")
    for sv in ket_qua:
        _, so_tien = xet_hoc_bong(sv[ky]["diem_hoc_luc"], sv[ky]["diem_ren_luyen"])
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv[ky]['diem_hoc_luc']}\t\t{sv[ky]['diem_ren_luyen']}\t\t{so_tien:,} VNĐ")

def tinh_gpa_ca_3_ky():
    """Tính GPA trung bình cả 3 kỳ của sinh viên"""
    if not danh_sach_sinh_vien:
        print("Danh sách sinh viên trống!")
        return
    print("\nGPA trung bình cả 3 kỳ:")
    print("Mã SV\tHọ tên\t\tGPA trung bình")
    for sv in danh_sach_sinh_vien:
        gpa_tb = (sv["hoc_ky_1"]["diem_hoc_luc"] + sv["hoc_ky_2"]["diem_hoc_luc"] + sv["hoc_ky_3"]["diem_hoc_luc"]) / 3
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{gpa_tb:.2f}")

def liet_ke_hoc_bong_ca_3_ky():
    """Liệt kê sinh viên nhận học bổng cả 3 kỳ"""
    ket_qua = []
    for sv in danh_sach_sinh_vien:
        tat_ca_ky_co_hoc_bong = True
        for ky in ["hoc_ky_1", "hoc_ky_2", "hoc_ky_3"]:
            if not xet_hoc_bong(sv[ky]["diem_hoc_luc"], sv[ky]["diem_ren_luyen"])[0]:
                tat_ca_ky_co_hoc_bong = False
                break
        if tat_ca_ky_co_hoc_bong:
            ket_qua.append(sv)
    if not ket_qua:
        print("Không có sinh viên nào nhận học bổng cả 3 kỳ!")
        return
    print("\nSinh viên nhận học bổng cả 3 kỳ:")
    print("Mã SV\tHọ tên\t\tKỳ 1 HL\tKỳ 1 RL\tKỳ 2 HL\tKỳ 2 RL\tKỳ 3 HL\tKỳ 3 RL")
    for sv in ket_qua:
        print(f"{sv['ma']}\t{sv['ho_ten']:<15}\t{sv['hoc_ky_1']['diem_hoc_luc']}\t{sv['hoc_ky_1']['diem_ren_luyen']}\t"
              f"{sv['hoc_ky_2']['diem_hoc_luc']}\t{sv['hoc_ky_2']['diem_ren_luyen']}\t"
              f"{sv['hoc_ky_3']['diem_hoc_luc']}\t{sv['hoc_ky_3']['diem_ren_luyen']}")

def main():
    """Hàm chính hiển thị menu và xử lý các lựa chọn"""
    doc_file()  # Đọc dữ liệu từ file khi khởi động
    while True:
        try:
            print("\n=== QUẢN LÝ SINH VIÊN NHẬN HỌC BỔNG ===")
            print("1. Thêm sinh viên")
            print("2. Hiển thị danh sách sinh viên")
            print("3. Cập nhật thông tin sinh viên")
            print("4. Xóa sinh viên")
            print("5. Thống kê và xét học bổng kỳ 1")
            print("6. Tìm kiếm sinh viên")
            print("7. Sắp xếp theo điểm học lực từ cao đến thấp kỳ 2")
            print("8. Liệt kê những sinh viên có GPA >= 8 kỳ 3")
            print("9. Sắp xếp theo điểm rèn luyện từ cao đến thấp kỳ 1")
            print("10. Liệt kê những sinh viên có điểm rèn luyện >= 80 kỳ 2")
            print("11. Sắp xếp theo tên")
            print("12. Liệt kê những sinh viên có học bổng kỳ 3")
            print("13. Liệt kê những sinh viên không có học bổng kỳ 1")
            print("14. Thống kê số lượng sinh viên theo mức học bổng kỳ 2")
            print("15. Liệt kê sinh viên theo khoảng điểm học lực kỳ 3")
            print("16. Liệt kê sinh viên theo khoảng điểm rèn luyện kỳ 1")
            print("17. Cập nhật tiêu chí học bổng")
            print("18. Hiển thị tiêu chí học bổng")
            print("19. Liệt kê những sinh viên có học bổng kỳ 2 trên 5 triệu")
            print("20. Liệt kê những sinh viên có học bổng kỳ 3 trên 8 triệu")
            print("21. Liệt kê những sinh viên có học bổng kỳ 1 trên 10 triệu")
            print("22. Tính điểm GPA cả 3 kỳ của sinh viên")
            print("23. Liệt kê những sinh viên được học bổng cả 3 học kỳ")
            print("24. Thoát chương trình")
            lua_chon = input("Nhập lựa chọn (1-24): ")
            if lua_chon == "1":
                them_sv()
            elif lua_chon == "2":
                hien_thi()
            elif lua_chon == "3":
                cap_nhat_thong_tin()
            elif lua_chon == "4":
                xoa_sinh_vien()
            elif lua_chon == "5":
                thong_ke_hoc_bong_ky("hoc_ky_1")
            elif lua_chon == "6":
                tim_kiem_sinh_vien()
            elif lua_chon == "7":
                sap_xep_theo_diem_hoc_luc_ky2()
            elif lua_chon == "8":
                liet_ke_gpa_8_ky3()
            elif lua_chon == "9":
                sap_xep_theo_diem_ren_luyen_ky1()
            elif lua_chon == "10":
                liet_ke_diem_ren_luyen_80_ky2()
            elif lua_chon == "11":
                sap_xep_theo_ten()
            elif lua_chon == "12":
                liet_ke_co_hoc_bong_ky3()
            elif lua_chon == "13":
                liet_ke_khong_co_hoc_bong_ky1()
            elif lua_chon == "14":
                thong_ke_muc_hoc_bong_ky2()
            elif lua_chon == "15":
                liet_ke_theo_khoang_diem_hoc_luc_ky3()
            elif lua_chon == "16":
                liet_ke_theo_khoang_diem_ren_luyen_ky1()
            elif lua_chon == "17":
                cap_nhat_ti_chi_hoc_bong()
            elif lua_chon == "18":
                hien_thi_ti_chi_hoc_bong()
            elif lua_chon == "19":
                liet_ke_hoc_bong_tren_muc_ky("hoc_ky_2", 5000000)
            elif lua_chon == "20":
                liet_ke_hoc_bong_tren_muc_ky("hoc_ky_3", 8000000)
            elif lua_chon == "21":
                liet_ke_hoc_bong_tren_muc_ky("hoc_ky_1", 10000000)
            elif lua_chon == "22":
                tinh_gpa_ca_3_ky()
            elif lua_chon == "23":
                liet_ke_hoc_bong_ca_3_ky()
            elif lua_chon == "24":
                print("Thoát chương trình!")
                break
            else:
                print("Lựa chọn không hợp lệ! Vui lòng chọn lại.")
        except EOFError:
            print("Lỗi nhập liệu, chương trình kết thúc!")
            break

if __name__ == "__main__":
    main()