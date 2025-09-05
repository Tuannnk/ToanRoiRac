# ========================
# Quine–McCluskey (SOP & POS)
# ========================

from typing import List, Tuple

# Chuyển số sang nhị phân
def to_bin(n: int, bits: int) -> str:
    return format(n, f"0{bits}b")

# Đếm số bit 1
def ones_count(s: str) -> int:
    return s.count("1")

# Khác đúng 1 bit
def diff_by_one_bit(a: str, b: str) -> Tuple[bool, int]:
    diff = 0
    pos = -1
    for i in range(len(a)):
        if a[i] != b[i]:
            diff += 1
            pos = i
            if diff > 1:
                return False, -1
    return diff == 1, pos

# Quine–McCluskey
def quine_mccluskey(minterms: List[int], bits: int) -> List[str]:
    groups = {}
    for m in minterms:
        b = to_bin(m, bits)
        groups.setdefault(ones_count(b), []).append(b)

    prime_implicants = set()
    changed = True

    while changed:
        changed = False
        new_groups = {}
        used = set()
        keys = sorted(groups.keys())
        for i in range(len(keys)-1):
            for a in groups[keys[i]]:
                for b in groups[keys[i+1]]:
                    ok, pos = diff_by_one_bit(a, b)
                    if ok:
                        changed = True
                        combined = a[:pos] + '-' + a[pos+1:]
                        new_groups.setdefault(ones_count(combined.replace("-", "")), []).append(combined)
                        used.add(a); used.add(b)
        # giữ lại PI
        for g in groups.values():
            for term in g:
                if term not in used:
                    prime_implicants.add(term)
        groups = {}
        for k, v in new_groups.items():
            groups[k] = list(set(v))
    return sorted(list(prime_implicants))

# Chuyển thành biểu thức SOP
def to_sop(term: str, vars: List[str]) -> str:
    res = []
    for i, ch in enumerate(term):
        if ch == "1": res.append(vars[i])
        elif ch == "0": res.append(vars[i] + "'")
    return "".join(res) if res else "1"

# Chuyển thành biểu thức POS
def to_pos(term: str, vars: List[str]) -> str:
    res = []
    for i, ch in enumerate(term):
        if ch == "1": res.append(vars[i] + "'")
        elif ch == "0": res.append(vars[i])
    return "(" + "+".join(res) + ")" if res else "(0)"

# ==========================
# CHƯƠNG TRÌNH CHÍNH
# ==========================
def main():
    num_vars = int(input("Nhập số biến (2,3,4): "))
    mode = input("Chọn mode (SOP/POS): ").strip().upper()
    terms = list(map(int, input("Nhập danh sách (cách nhau bằng dấu phẩy): ").split(",")))

    all_terms = set(range(2**num_vars))
    if mode == "POS":
        # maxterm -> chuyển thành minterm còn lại
        terms = list(all_terms - set(terms))

    pis = quine_mccluskey(terms, num_vars)

    print("\nPrime Implicants:")
    for pi in pis:
        if mode == "SOP":
            print(f"{pi}  ->  {to_sop(pi, [chr(65+i) for i in range(num_vars)])}")
        else:
            print(f"{pi}  ->  {to_pos(pi, [chr(65+i) for i in range(num_vars)])}")

if __name__ == "__main__":
    main()
