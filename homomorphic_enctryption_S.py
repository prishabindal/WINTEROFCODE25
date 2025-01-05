# import random
# from math import gcd
# from sympy import isprime, mod_inverse
# import base64

# def lcm(a, b):
#     """Calculate the Least Common Multiple of a and b."""
#     return abs(a * b) // gcd(a, b)

# def generate_prime(bits=512):
#     """Generate a random prime number with the specified bit length."""
#     while True:
#         p = random.getrandbits(bits)
#         if isprime(p):
#             return p

# def generate_paillier_keys(bits=512):
#     """
#     Generate Paillier public and private keys.
#     - Public key: (n, g)
#     - Private key: (lambda, mu)
#     """
#     # Step 1: Generate two large prime numbers
#     p = generate_prime(bits)
#     q = generate_prime(bits)
#     while p == q:  # Ensure p and q are distinct
#         q = generate_prime(bits)

#     # Step 2: Compute n and n^2
#     n = p * q
#     n_sq = n ** 2

#     # Step 3: Compute λ (lambda), the Carmichael's totient function of n
#     λ = lcm(p - 1, q - 1)

#     # Step 4: Choose g and calculate μ (mu)
#     g = n + 1  # Common choice for g
#     μ = mod_inverse(λ, n)  # Modular multiplicative inverse of λ mod n

#     # Public and private keys
#     public_key = (n, g)
#     private_key = (λ, μ)

#     return public_key, private_key



# def text_to_int(text):
#     if isinstance(text, int):
#         return text
#     return int.from_bytes(text.encode('utf-8'), 'big')

# def int_to_text(number):
#     return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')

# def encrypt(plaintext, public_key):
#     n, g = public_key
#     n_sq = n ** 2
#     r = random.randint(1, n - 1)
#     while gcd(r, n) != 1:
#         r = random.randint(1, n - 1)
    
#     number = text_to_int(plaintext)
#     ciphertext = (pow(g, number, n_sq) * pow(r, n, n_sq)) % n_sq
#     ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')
#     encoded = base64.b64encode(ciphertext_bytes)
#     return encoded

# def decrypt(encoded_ciphertext, public_key, private_key):
#     n, _ = public_key
#     n_sq = n ** 2
#     λ, μ = private_key

#     ciphertext_bytes = base64.b64decode(encoded_ciphertext)
    
#     # Convert bytes back to integer
#     ciphertext_number = int.from_bytes(ciphertext_bytes, 'big')
    
#     c_lambda = pow(ciphertext_number), λ, n_sq
#     L_c_lambda = (c_lambda - 1) // n
#     plaintext_num = (L_c_lambda * μ) % n
#     return int_to_text(plaintext_num)

# if __name__ == "__main__":
#     public_key, private_key = generate_paillier_keys(bits=512)
    
#     message = "Hello World!"
#     print("\nOriginal message:", message)
    
#     # ciphertext = encrypt(message, public_key)
#     ciphertext = 786905582582373882534344302668995706635643253032400933674798121792052601269212320468704622854373001749478927511192512050751773222668720465847184295423132715764988714862894062971487486342740015182123848747705027849403633406728574903655876696148703938163405263338568680283173112358628827433503004068923684338390176046197226055228510136716349240785311383172551521468276458042147933036216112831454955026338161518792190170662676103159431455224881915229455232444580619624748114565308696531395813187049623634138828480680729841484580480266574644699625756009499689952525207838923421261424319888786387797225455738400593485175
#     print("Encrypted:", ciphertext)
    
#     decrypted = decrypt(ciphertext, public_key, private_key)
#     print("Decrypted:", decrypted)
import random
from math import gcd
from sympy import isprime, mod_inverse
import base64

def lcm(a, b):
    """Calculate the Least Common Multiple of a and b."""
    return abs(a * b) // gcd(a, b)

def generate_prime(bits=512):
    """Generate a random prime number with the specified bit length."""
    while True:
        p = random.getrandbits(bits)
        if isprime(p):
            return p

def generate_paillier_keys(bits=512):
    """
    Generate Paillier public and private keys.
    - Public key: (n, g)
    - Private key: (lambda, mu)
    """
    # Step 1: Generate two large prime numbers
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:  # Ensure p and q are distinct
        q = generate_prime(bits)

    # Step 2: Compute n and n^2
    n = p * q
    n_sq = n ** 2

    # Step 3: Compute λ (lambda), the Carmichael's totient function of n
    λ = lcm(p - 1, q - 1)

    # Step 4: Choose g and calculate μ (mu)
    g = n + 1  # Common choice for g
    μ = mod_inverse(λ, n)  # Modular multiplicative inverse of λ mod n

    return (n, g), (λ, μ)

def text_to_int(text):
    if isinstance(text, int):
        return text
    return int.from_bytes(text.encode('utf-8'), 'big')

def int_to_text(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')

def encrypt(plaintext, public_key):
    n, g = public_key
    n_sq = n ** 2
    r = random.randint(1, n - 1)
    while gcd(r, n) != 1:
        r = random.randint(1, n - 1)
    
    number = text_to_int(plaintext)
    ciphertext = (pow(g, number, n_sq) * pow(r, n, n_sq)) % n_sq
    ciphertext_string = str(ciphertext)
    ciphertext_bytes = ciphertext.to_bytes((ciphertext.bit_length() + 7) // 8, 'big')
    
    return ciphertext_string

def decrypt(encoded_ciphertext, public_key, private_key):
    n, _ = public_key
    n_sq = n ** 2
    λ, μ = private_key

    # ciphertext_bytes = base64.b64decode(encoded_ciphertext)
    
    # ciphertext_number = int.from_bytes(encoded_ciphertext, 'big')
    ciphertext_number = int(encoded_ciphertext)
    
    # Fix: Remove extra parenthesis in pow() call
    c_lambda = pow(ciphertext_number, λ, n_sq)
    L_c_lambda = (c_lambda - 1) // n
    plaintext_num = (L_c_lambda * μ) % n
    plaintext = int_to_text(plaintext_num)
    return plaintext

if __name__ == "__main__":
    public_key, private_key = generate_paillier_keys(bits=512)
    
    message = "1234"
    print("\nOriginal message:", message)
    
    ciphertext = encrypt(message, public_key)
    print("Encrypted:", ciphertext)
    
    decrypted = decrypt(ciphertext, public_key, private_key)
    print("Decrypted:", decrypted)