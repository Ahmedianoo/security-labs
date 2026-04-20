"""
LAB A — RSA Encryption & Decryption

In this lab you will:
  1. Implement the core modular arithmetic primitives (GCD, Extended Euclidean, modular inverse).
  2. Build RSA key-pair generation from two given primes.
  3. Encrypt and decrypt single numeric messages.
  4. Encrypt and decrypt text strings 
"""

# A set of known primes to pick from.
# You MUST choose two DISTINCT primes from this list
PRIME_LIST = [
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
    199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
]

# 311, 313
# ┌──────────────────────────────────────────────────────────────────────┐
# │  PART 1 — Mathematical Foundations                                   │
# └──────────────────────────────────────────────────────────────────────┘

def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """Extended Euclidean Algorithm.

    Returns (g, x, y) such that  a*x + b*y == g == gcd(a, b).
    """
    # Variables initialization for the extended Euclidean algorithm.
    # Matching the lecture table (slide 12):
    #   r_{i-2}, r_{i-1}  start as  a, b
    #   x_{i-2}, x_{i-1}  start as  1, 0
    #   y_{i-2}, y_{i-1}  start as  0, 1
    
    r_old, r_cur = a, b
    x_old, x_cur = 1, 0
    y_old, y_cur = 0, 1

    # TODO: Implement the extended Euclidean algorithm.
    while(r_cur != 0):
        q = r_old // r_cur
        r_temp, x_temp, y_temp = r_cur, x_cur, y_cur

        r_cur = r_old % r_cur
        x_cur = x_old - (q * x_cur)
        y_cur = y_old - (q * y_cur)

        r_old, x_old, y_old =r_temp, x_temp, y_temp

    return r_old, x_old, y_old


def mod_inverse(e: int, phi: int) -> int:
    """Compute the modular multiplicative inverse of e mod phi.
    """
    # TODO: Use your extended_gcd function above.

    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Inverse does not exist")
    
    return x % phi

# ┌──────────────────────────────────────────────────────────────────────┐
# │  PART 2 — RSA Key Generation                                        │
# └──────────────────────────────────────────────────────────────────────┘

def generate_keypair(p: int, q: int) -> dict:
    """Generate an RSA key pair from two chosen primes p and q.

    Returns a dict with keys:
        "p", "q"       — the two primes
        "e"            — public exponent (must satisfy gcd(e, phi)==1)
        "d"            — private exponent (modular inverse of e mod phi)
    """
    # TODO: Implement RSA key generation.
    #   Verify p != q.
    if(p == q):
        raise ValueError("q and p cannot be equal to each other")
    
    phi = (p -1) * (q - 1)

    #   Loop until you find e such that gcd(e, phi) == 1.
    e = 2
    while(e != 1):
        g, _, _ = extended_gcd(e, phi) 

        if g == 1:
            break

        e += 1

    #   Compute d 
    d = mod_inverse(e, phi)

    #   Return the dict described above.
    return {
        "q": q, 
        "p": p, 
        "e": e, 
        "d": d
    }


# ┌──────────────────────────────────────────────────────────────────────┐
# │  PART 3 — Encryption & Decryption                                   │
# └──────────────────────────────────────────────────────────────────────┘

def encrypt_number(m: int, public_key: tuple[int, int]) -> int:
    """Encrypt a single integer m using the RSA public key.
    """
    # TODO: Validate m, then compute cipher-text c.
    #       Hint: use pow() for modular exponentiation.
    if (m >= public_key[1]):
        raise ValueError("m must be less than n")
    
    return pow(m, public_key[0], public_key[1])


def decrypt_number(c: int, private_key: tuple[int, int]) -> int:
    """Decrypt a single integer c using the RSA private key (d, n).

    Plaintext m = c^d mod n.
    """
    # TODO: Compute the plaintext m from c.
    #       Hint: use pow() for modular exponentiation.
    return pow(c, private_key[0], private_key[1])


def encrypt_text(plaintext: str, public_key: tuple[int, int]) -> list[int]:
    """Encrypt a text string into a list of integers using the RSA public key.
    """
    # TODO: For each character in plaintext:
    #   1. Convert to ASCII ordinal.
    #   2. Encrypt
    #   Return the list of ciphertext integers.
    return [encrypt_number(ord(char), public_key) for char in plaintext]


def decrypt_text(ciphertext: list[int], private_key: tuple[int, int]) -> str:
    """Decrypt a list of ciphertext integers back to a string.
    """
    # TODO: For each ciphertext integer:
    #   1. Decrypt to get the ASCII ordinal.
    #   2. Convert back to a character
    #   Return the joined string.
    return ''.join(chr(decrypt_number(c, private_key)) for c in ciphertext)


# ┌──────────────────────────────────────────────────────────────────────┐
# │  PART 4 — Demonstrate the Fundamental RSA Property                   │
# └──────────────────────────────────────────────────────────────────────┘

def verify_rsa_property(m: int, e: int, d: int, n: int) -> bool:
    """Verify that M^(e*d) mod n == M  (the fundamental RSA identity).
    """
    # TODO: Verify the RSA identity and return True/False.
    #       Hint: use pow() for modular exponentiation.
    return pow(m, (e*d), n) == m


# ┌──────────────────────────────────────────────────────────────────────┐
# │  PART 5 — Interactive Demo                                           │
# └──────────────────────────────────────────────────────────────────────┘

def run_demo():

    print("\n[1] Generating RSA key pair")
    # Pick p and q from PRIME_LIST, and they must be distinct.
    keys = generate_keypair(251, 257)
    p, q, e, d = keys['p'], keys['q'], keys['e'], keys['d']

    # TODO: Compute n, phi, public_key, private_key from keys dict.
    n = p * q
    phi = (p - 1) * (q - 1)
    public_key = (e, n)
    private_key = (d, n)

    # TODO: Print out all the key components in a nice format.
    print(f"    p = {p}")
    print(f"    q = {q}")
    print(f"    n = {n}")
    print(f"    φ(n) = {phi}")
    print(f"    e = {e}")
    print(f"    d = {d}")
    print(f"    Public key = {public_key}")
    print(f"    Private key = {private_key}")


    print("\n[2] Encrypting a single number...")
    m = 42
    # TODO: Encrypt m
    c = encrypt_number(m, public_key)
    print(f"    Plaintext  M = {m}")
    print(f"    Ciphertext C = {c}")


    print("\n[3] Decrypting back...")
    # TODO: Decrypt c
    m_dec = decrypt_number(c, private_key)
    print(f"    Decrypted  M = {m_dec}")
    assert m_dec == m, "DECRYPTION FAILED!"
    print("    ✓ Decryption matches original!")


    print("\n[4] Verifying the fundamental RSA property...")
    # TODO: Verify the RSA property
    ok = verify_rsa_property(m, e, d, n)
    print(f"    M^(e·d) mod n == M ? {ok}")
    assert ok, "RSA PROPERTY FAILED!"
    print("    ✓ Fundamental RSA property holds!")


    print("\n[5] Encrypting a text message...")
    message = "RSA works!"
    print(f'    Plaintext: "{message}"')
    # TODO: Encrypt the message
    ct = encrypt_text(message, public_key)
    print(f"    Ciphertext: {ct}")

    # TODO: Decrypt the message
    pt = decrypt_text(ct, private_key)
    print(f'    Decrypted:  "{pt}"')
    assert pt == message, "TEXT DECRYPTION FAILED!"
    print("    ✓ Text round-trip successful!")


if __name__ == "__main__": 
    run_demo()
