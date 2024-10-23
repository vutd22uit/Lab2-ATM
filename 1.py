import random
import math
from typing import List, Tuple

class NumberTheory:
    @staticmethod
    def is_prime(n: int) -> bool:
        """Kiểm tra số nguyên tố bằng Miller-Rabin"""
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False

        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        
        for a in bases:
            if a >= n:
                break
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            
            for _ in range(r - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def generate_prime(bits: int) -> int:
        """Tạo số nguyên tố ngẫu nhiên với số bit cho trước"""
        while True:
            n = random.getrandbits(bits)
            n |= (1 << bits - 1)
            n |= 1
            if NumberTheory.is_prime(n):
                return n

    @staticmethod
    def mersenne_prime(p: int) -> int:
        """Tính số Mersenne Mp = 2^p - 1"""
        return (1 << p) - 1

    @staticmethod
    def find_mersenne_primes(limit: int) -> List[Tuple[int, int]]:
        """Tìm các số Mersenne prime đầu tiên"""
        mersenne_primes = []
        potential_exponents = [2, 3, 5, 7, 13, 17, 19, 31, 61, 89]
        
        for p in potential_exponents:
            mp = NumberTheory.mersenne_prime(p)
            if NumberTheory.is_prime(mp):
                mersenne_primes.append((p, mp))
                if len(mersenne_primes) >= limit:
                    break
        return mersenne_primes

    @staticmethod
    def find_largest_primes_under(n: int, count: int) -> List[int]:
        """Tìm count số nguyên tố lớn nhất nhỏ hơn n"""
        primes = []
        current = n - 1
        while len(primes) < count and current > 1:
            if NumberTheory.is_prime(current):
                primes.append(current)
            current -= 1
        return primes

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Tính ước chung lớn nhất"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def mod_exp(base: int, exponent: int, modulus: int) -> int:
        """Tính lũy thừa modulo"""
        if modulus == 1:
            return 0
        result = 1
        base = base % modulus
        while exponent > 0:
            if exponent & 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent >>= 1
        return result

def print_menu():
    """Hiển thị menu chương trình"""
    print("\n=== CHƯƠNG TRÌNH SỐ HỌC ===")
    print("1. Tạo số nguyên tố ngẫu nhiên (8, 16, 64 bits)")
    print("2. Tìm 10 số nguyên tố lớn nhất dưới 10 số Mersenne prime đầu")
    print("3. Kiểm tra số nguyên tố < 2^89-1")
    print("4. Tính ước chung lớn nhất (GCD)")
    print("5. Tính lũy thừa modulo (a^x mod p)")
    print("0. Thoát")
    return input("Chọn chức năng (0-5): ")

def main():
    nt = NumberTheory()
    
    while True:
        choice = print_menu()
        
        if choice == "0":
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
            
        elif choice == "1":
            try:
                bits = int(input("\nNhập số bits (8, 16, hoặc 64): "))
                if bits not in [8, 16, 64]:
                    print("Vui lòng chọn 8, 16 hoặc 64 bits!")
                    continue
                prime = nt.generate_prime(bits)
                print(f"\nSố nguyên tố {bits} bits: {prime}")
                print(f"Dạng nhị phân: {bin(prime)[2:]}")
                print(f"Số bits thực tế: {len(bin(prime))-2}")
            except ValueError:
                print("Vui lòng nhập số nguyên hợp lệ!")
                
        elif choice == "2":
            try:
                print("\n=== 10 SỐ MERSENNE PRIME ĐẦU TIÊN VÀ CÁC SỐ NGUYÊN TỐ LỚN NHẤT ===")
                mersenne_primes = nt.find_mersenne_primes(10)
                
                for i, (p, mp) in enumerate(mersenne_primes, 1):
                    print(f"\nM{i} = 2^{p} - 1 = {mp}")
                    largest_primes = nt.find_largest_primes_under(mp, 10)
                    print(f"10 số nguyên tố lớn nhất nhỏ hơn M{i}:")
                    for j, prime in enumerate(largest_primes, 1):
                        print(f"{j}. {prime}")
            except Exception as e:
                print(f"Có lỗi xảy ra: {e}")
                
        elif choice == "3":
            try:
                limit = 2**89 - 1
                print(f"\nKiểm tra số nguyên tố < 2^89-1 ({limit})")
                while True:
                    try:
                        n = int(input("Nhập số cần kiểm tra (nhập 0 để quay lại menu chính): "))
                        if n == 0:
                            break
                        if n < 0 or n >= limit:
                            print(f"Vui lòng nhập số trong khoảng [1, {limit-1}]")
                            continue
                        result = nt.is_prime(n)
                        print(f"{n} {'là số nguyên tố' if result else 'không phải số nguyên tố'}")
                    except ValueError:
                        print("Vui lòng nhập số nguyên hợp lệ!")
            except Exception as e:
                print(f"Có lỗi xảy ra: {e}")
                
        elif choice == "4":
            try:
                print("\n=== TÍNH ƯỚC CHUNG LỚN NHẤT ===")
                a = int(input("Nhập số thứ nhất: "))
                b = int(input("Nhập số thứ hai: "))
                if a < 0 or b < 0:
                    print("Vui lòng nhập số không âm!")
                    continue
                result = nt.gcd(a, b)
                print(f"\nƯớc chung lớn nhất của {a} và {b} là: {result}")
            except ValueError:
                print("Vui lòng nhập số nguyên hợp lệ!")
                
        elif choice == "5":
            try:
                print("\n=== TÍNH LŨY THỪA MODULO ===")
                base = int(input("Nhập cơ số (a): "))
                exponent = int(input("Nhập số mũ (x): "))
                modulus = int(input("Nhập modulo (p): "))
                if modulus <= 0:
                    print("Modulo phải là số dương!")
                    continue
                result = nt.mod_exp(base, exponent, modulus)
                print(f"\n{base}^{exponent} mod {modulus} = {result}")
            except ValueError:
                print("Vui lòng nhập số nguyên hợp lệ!")
                
        else:
            print("Vui lòng chọn chức năng hợp lệ!")

if __name__ == "__main__":
    main()