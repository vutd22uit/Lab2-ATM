import random
import math
from typing import Tuple, Union

def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_value: int = 100, max_value: int = 1000) -> int:
    prime = random.randrange(min_value, max_value)
    while not is_prime(prime):
        prime = random.randrange(min_value, max_value)
    return prime

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e: int, phi: int) -> int:
    def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    _, d, _ = extended_gcd(e, phi)
    return d % phi

def generate_keypair(p: int = None, q: int = None, e: int = None) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA key pair either from given p, q, e or randomly.
    Returns ((e, n), (d, n)) representing (public_key, private_key)
    """
    # If p and q are not provided, generate random primes
    if p is None or q is None:
        p = generate_prime()
        q = generate_prime()
        while p == q:  # Ensure p and q are different
            q = generate_prime()
    
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime numbers")

    n = p * q
    phi = (p - 1) * (q - 1)

    # If e is not provided, generate suitable e
    if e is None:
        e = random.randrange(2, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(2, phi)
    else:
        if gcd(e, phi) != 1:
            raise ValueError("e must be coprime to phi")

    # Calculate private key
    d = mod_inverse(e, phi)

    return ((e, n), (d, n))

def encrypt(public_key: Tuple[int, int], message: Union[str, int]) -> list:
    e, n = public_key
    if isinstance(message, str):
        # Convert string to numbers (using ASCII values)
        return [pow(ord(char), e, n) for char in message]
    else:
        return [pow(message, e, n)]

def decrypt(private_key: Tuple[int, int], encrypted_msg: list) -> Union[str, int]:
    d, n = private_key
    decrypted = [pow(char, d, n) for char in encrypted_msg]
    
    # Try to convert back to string if possible
    try:
        return ''.join(chr(char) for char in decrypted)
    except ValueError:
        # If conversion fails, return the number
        return decrypted[0] if len(decrypted) == 1 else decrypted

def main():
    print("=== Chương trình minh họa RSA ===")
    print("\nBạn muốn:")
    print("1. Tự nhập p, q, e")
    print("2. Để chương trình tự tạo khóa ngẫu nhiên")
    choice = input("Lựa chọn của bạn (1/2): ")

    try:
        if choice == "1":
            # Nhập p, q, e từ người dùng
            print("\nNhập các số nguyên tố p, q và e:")
            p = int(input("Nhập p: "))
            q = int(input("Nhập q: "))
            e = int(input("Nhập e: "))
            
            # Kiểm tra tính hợp lệ của đầu vào
            if not is_prime(p) or not is_prime(q):
                raise ValueError("p và q phải là số nguyên tố!")
            
            public_key, private_key = generate_keypair(p, q, e)
        else:
            # Tự động tạo khóa
            print("\nĐang tạo khóa ngẫu nhiên...")
            public_key, private_key = generate_keypair()

        print(f"\nKhóa công khai (e, n): {public_key}")
        print(f"Khóa bí mật (d, n): {private_key}")

        print("\nBạn muốn mã hóa:")
        print("1. Số nguyên")
        print("2. Chuỗi văn bản")
        msg_type = input("Lựa chọn của bạn (1/2): ")

        if msg_type == "1":
            message = int(input("\nNhập số cần mã hóa: "))
        else:
            message = input("\nNhập chuỗi cần mã hóa: ")

        # Mã hóa
        print("\nĐang thực hiện mã hóa...")
        encrypted_msg = encrypt(public_key, message)
        print(f"Thông điệp đã mã hóa: {encrypted_msg}")

        # Giải mã
        print("\nĐang thực hiện giải mã...")
        decrypted_msg = decrypt(private_key, encrypted_msg)
        print(f"Thông điệp sau khi giải mã: {decrypted_msg}")

        # Kiểm tra
        print("\nKiểm tra kết quả:", "Thành công!" if str(decrypted_msg) == str(message) else "Thất bại!")

    except ValueError as e:
        print(f"\nLỗi: {e}")
    except Exception as e:
        print(f"\nĐã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()