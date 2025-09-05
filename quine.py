from collections import defaultdict
from typing import List, Set, Tuple, Dict

# ===================== Hàm phụ trợ =====================
def to_bin(n: int, bits: int) -> str:
    # Chuyển số nguyên n sang chuỗi nhị phân có độ dài bits
    return format(n, f"0{bits}b")

def ones_count(s: str) -> int:
    # Đếm số lượng bit 1 trong chuỗi nhị phân
    return s.count("1")

def pattern_to_expr(pattern: str, var_names: List[str]) -> str:
    """Chuyển pattern (chuỗi 0/1/-) thành biểu thức Boolean.
    Ví dụ: '10-1' với biến [A,B,C,D] -> A B' D"""
    terms = []
    for ch, v in zip(pattern, var_names):
        if ch == '-':
            continue  # '-' tức là không phụ thuộc biến này
        terms.append(v if ch == '1' else f"{v}'")
    return ''.join(terms) if terms else '1'

# ===================== Lõi Quine–McCluskey =====================
class Implicant:
    def __init__(self, pattern: str, covers: Set[int]):
        self.pattern = pattern  # mẫu, ví dụ '10-1'
        self.covers = set(covers)  # tập hợp các minterm mà mẫu này phủ
        self.merged = False  # đánh dấu xem đã được ghép ở vòng sau chưa

    def __repr__(self):
        return f"Implicant({self.pattern}, {sorted(self.covers)})"


def can_combine(a: str, b: str) -> Tuple[bool, str]:
    """Kiểm tra có thể ghép 2 mẫu a và b hay không.
    Chỉ ghép được nếu khác nhau đúng 1 vị trí (0/1) và không liên quan tới '-'.
    """
    diff = 0
    out = []
    for x, y in zip(a, b):
        if x == y:
            out.append(x)
        else:
            if x == '-' or y == '-':
                return False, ''  # nếu có '-' thì không ghép
            diff += 1
            out.append('-')
            if diff > 1:
                return False, ''
    return (diff == 1, ''.join(out))


def initial_groups(minterms: List[int], num_vars: int) -> Dict[int, List[Implicant]]:
    # Nhóm minterm ban đầu theo số lượng bit 1
    groups: Dict[int, List[Implicant]] = defaultdict(list)
    for m in sorted(set(minterms)):
        bits = to_bin(m, num_vars)
        groups[ones_count(bits)].append(Implicant(bits, {m}))
    return groups


def next_round(groups: Dict[int, List[Implicant]]) -> Tuple[Dict[int, List[Implicant]], List[Implicant]]:
    """Thực hiện một vòng ghép nhóm, trả về (nhóm mới, các PI được xác định)."""
    new_groups: Dict[int, List[Implicant]] = defaultdict(list)
    produced = set()  # để tránh trùng lặp

    keys = sorted(groups.keys())
    for i in range(len(keys) - 1):
        g1 = groups[keys[i]]
        g2 = groups[keys[i + 1]]
        for a in g1:
            for b in g2:
                ok, comb = can_combine(a.pattern, b.pattern)
                if ok:
                    a.merged = True
                    b.merged = True
                    key = (comb, tuple(sorted(a.covers | b.covers)))
                    if key not in produced:
                        new_groups[ones_count(comb.replace('-', ''))].append(
                            Implicant(comb, a.covers | b.covers)
                        )
                        produced.add(key)

    # Những implicant không được ghép sẽ trở thành prime implicant
    primes: List[Implicant] = []
    for g in groups.values():
        for imp in g:
            if not imp.merged:
                primes.append(imp)
    return new_groups, primes


def find_prime_implicants(minterms: List[int], num_vars: int) -> List[Implicant]:
    # Vòng lặp ghép nhóm cho đến khi không còn ghép được
    groups = initial_groups(minterms, num_vars)
    primes: List[Implicant] = []
    while groups:
        groups, round_primes = next_round(groups)
        primes.extend(round_primes)
    return primes


def prime_implicant_chart(primes: List[Implicant], minterms: List[int]) -> Dict[str, Set[int]]:
    # Tạo bảng phủ: mỗi prime implicant -> tập các minterm mà nó phủ
    chart: Dict[str, Set[int]] = {}
    for p in primes:
        covered = set()
        for m in minterms:
            if covers_pattern(p.pattern, m):
                covered.add(m)
        chart[p.pattern] = covered
    return chart


def covers_pattern(pattern: str, m: int) -> bool:
    # Kiểm tra một mẫu có phủ một minterm hay không
    bits = to_bin(m, len(pattern))
    return all(pc == '-' or pc == bc for pc, bc in zip(pattern, bits))


def find_essential_pis(chart: Dict[str, Set[int]], minterms: List[int]) -> Tuple[Set[str], Set[int]]:
    # Tìm các essential prime implicant (EPI)
    essential: Set[str] = set()
    for m in minterms:
        owners = [p for p, cols in chart.items() if m in cols]
        if len(owners) == 1:
            essential.add(owners[0])
    covered = set()
    for p in essential:
        covered |= chart[p]
    return essential, covered


def greedy_cover(chart: Dict[str, Set[int]], minterms: List[int], already: Set[int]) -> Set[str]:
    # Phủ các minterm còn lại bằng chiến lược tham lam
    remaining = set(minterms) - already
    chosen: Set[str] = set()
    while remaining:
        best = None
        best_gain = -1
        for p, cols in chart.items():
            gain = len(cols & remaining)
            if gain > best_gain:
                best_gain = gain
                best = p
        if best is None or best_gain <= 0:
            break
        chosen.add(best)
        remaining -= chart[best]
    return chosen


def quine_mccluskey(minterms: List[int], num_vars: int, var_names: List[str] | None = None):
    # Thực hiện toàn bộ thuật toán Quine–McCluskey
    if var_names is None:
        var_names = [chr(ord('A') + i) for i in range(num_vars)]

    primes = find_prime_implicants(minterms, num_vars)
    primes = sorted(primes, key=lambda imp: (-imp.pattern.count('-'), imp.pattern))

    chart = prime_implicant_chart(primes, minterms)
    essential, covered = find_essential_pis(chart, minterms)
    extra = greedy_cover(chart, minterms, covered)

    selected = sorted(essential | extra, key=lambda p: (-p.count('-'), p))
    expr_terms = [pattern_to_expr(p, var_names) for p in selected]
    simplified_expr = ' + '.join(expr_terms) if expr_terms else '0'

    return {
        'prime_implicants': [imp.pattern for imp in primes],
        'chart': {p: sorted(cols) for p, cols in chart.items()},
        'essential_prime_implicants': sorted(list(essential)),
        'additional_implicants': sorted(list(extra - essential)),
        'selected_implicants': selected,
        'simplified_expression': simplified_expr,
    }

# ===================== Giao diện CLI / Demo =====================

def _read_int_list(s: str) -> List[int]:
    # Chuyển chuỗi nhập vào thành list số nguyên
    out = []
    for part in s.replace(',', ' ').split():
        if part.strip():
            out.append(int(part))
    return out


def main():
    print("=== Quine–McCluskey (SOP) ===")
    num_vars = int(input("Nhập số biến (>=2): ").strip())
    var_names = [chr(ord('A') + i) for i in range(num_vars)]
    minterms = _read_int_list(input("Nhập danh sách minterm, ví dụ: 0,1,2,5,6,7,8,9,10,14\n> "))

    res = quine_mccluskey(minterms, num_vars, var_names)

    print("\nPrime implicants (PI):")
    for p in res['prime_implicants']:
        print("  ", p, "->", pattern_to_expr(p, var_names))

    print("\nBảng phủ (PI -> minterm phủ):")
    for p, cols in res['chart'].items():
        print(f"  {p}: {cols}")

    print("\nEssential prime implicants (EPI):")
    for p in res['essential_prime_implicants']:
        print("  ", p, "->", pattern_to_expr(p, var_names))

    if res['additional_implicants']:
        print("\nCác implicant bổ sung (greedy cover):")
        for p in res['additional_implicants']:
            print("  ", p, "->", pattern_to_expr(p, var_names))

    print("\nCác implicant được chọn:")
    for p in res['selected_implicants']:
        print("  ", p, "->", pattern_to_expr(p, var_names))

    print("\nBiểu thức tối giản:")
    print("  f =", res['simplified_expression'])

if __name__ == '__main__':
    main()


# ========================
# Quine–McCluskey Example
# ========================

from typing import List, Tuple

# Chuyển số sang dạng nhị phân cố định độ dài
def to_bin(n: int, bits: int) -> str:
    return format(n, f"0{bits}b")

# Đếm số bit 1
def ones_count(s: str) -> int:
    return s.count("1")

# Kiểm tra 2 chuỗi nhị phân khác đúng 1 bit
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

# Gom nhóm minterm thành prime implicants
def quine_mccluskey(minterms: List[int], bits: int) -> List[str]:
    groups = {}
    for m in minterms:
        b = to_bin(m, bits)
        groups.setdefault(ones_count(b), []).append(b)

    prime_implicants = set()
    marked = set()
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
        # Các term không được dùng -> prime implicant
        for g in groups.values():
            for term in g:
                if term not in used:
                    prime_implicants.add(term)
        groups = {}
        # bỏ trùng
        for k, v in new_groups.items():
            groups[k] = list(set(v))
    return sorted(list(prime_implicants))

# Hàm in biểu thức
def to_expr(term: str, vars: List[str]) -> str:
    res = []
    for i, ch in enumerate(term):
        if ch == "1": res.append(vars[i])
        elif ch == "0": res.append(vars[i] + "'")
    return "".join(res) if res else "1"

# =====================
# CHẠY VÍ DỤ BÀI TẬP
# =====================
print("Bài 1: f(A,B,C) = Σm(1,2,5,7)")
pis = quine_mccluskey([1,2,5,7], 3)
for pi in pis:
    print(f"{pi}  ->  {to_expr(pi, ['A','B','C'])}")

print("\nBài 2: f(A,B,C,D) = Σm(0,2,5,7,8,10,13,15)")
pis = quine_mccluskey([0,2,5,7,8,10,13,15], 4)
for pi in pis:
    print(f"{pi}  ->  {to_expr(pi, ['A','B','C','D'])}")
