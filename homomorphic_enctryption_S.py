import random
from math import gcd
from sympy import isprime, mod_inverse
import Globals

def lcm(a, b):
    """Calculate the Least Common Multiple of a and b."""
    return abs(a * b) // gcd(a, b)

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

#     return (n, g), (λ, μ)

def text_to_int(text):
    if isinstance(text, int):
        return text
    return int.from_bytes(text.encode('utf-8'), 'big')

def int_to_text(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big').decode('utf-8')

def encrypt(plaintext, public_key):
    n, g = public_key
    n_sq = n ** 2
    # r = random.randint(1, n - 1)
    # while gcd(r, n) != 1:
    #     r = random.randint(1, n - 1)

    r=1
    
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
    private_key = (44298812690117117666694631195833862099871623702009383333199226570511257188480020812305235721726410432412844572466393920148493790417441048946892057963724112128845975874073175595217101068298442741713655227723989191606198294526026574256713068062189122729883065007267718130711556540451635992010667359111597635916, 85620423307565838183396836313409037014450494511368681575067376014236441230991057967192317689371424511307827904199974532602306453575165191709065301539223363918287662344091565122333021473403391202641425642397146747446991303821113770096193118929144460729708795148005404232464502202867560996569248563565819645390)
    public_key = (88597625380234235333389262391667724199743247404018766666398453141022514376960041624610471443452820864825689144932787840296987580834882097893784115927448243158322082013265147305559691067950092517726883608838852238643596414510629499939255547534772534127426999277633760492895060272098932013964000465314329885731, 88597625380234235333389262391667724199743247404018766666398453141022514376960041624610471443452820864825689144932787840296987580834882097893784115927448243158322082013265147305559691067950092517726883608838852238643596414510629499939255547534772534127426999277633760492895060272098932013964000465314329885732)
    
    message = "prisha06"
    print("\nOriginal message:", message)
    print(Globals.public_key)
    
    ciphertext = encrypt(message, public_key)
    print("Encrypted:", ciphertext)
    
    decrypted = decrypt(ciphertext, public_key, private_key)
    print("Decrypted:", decrypted)
    