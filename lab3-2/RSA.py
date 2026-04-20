import hashlib

"""
LAB B — RSA Digital Signatures

In this lab you will:
  1. Implement the core modular arithmetic primitives (GCD, Extended Euclidean, modular inverse).
  2. Build RSA key-pair generation from two given primes.
  3. Hash a text message into a numeric value using SHA-256.
  4. Sign numeric and text messages using the RSA private key.
  5. Verify signatures using the RSA public key.
  6. Run a forgery experiment to see that altering a message invalidates its signature.
"""

# A set of known primes to pick from.
# You MUST choose two DISTINCT primes from this list
AVAILABLE_PRIMES = [
    101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
    151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
    199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
]

# ======================================================================
#  SECTION 1 :  Modular Arithmetic Toolkit
# ======================================================================
#  Implement each function.  They are used everywhere else in the lab.
# ======================================================================


def extended_euclidean(a, b) -> tuple[int, int, int]:
    """Return (g, x, y) with  a*x + b*y == g == gcd(a, b).

    Use the tabular / iterative form (not recursion).
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
        x_cur = x_old - (x_cur * q)
        y_cur = y_old - (y_cur * q)

        r_old, x_old, y_old = r_temp, x_temp, y_temp

    return r_old, x_old, y_old ## 


def find_modular_inverse(e, phi) -> int:
    """Compute the modular multiplicative inverse of e mod phi.
    """
    # TODO: Use your extended_gcd function above.
    #       Make sure d is positive (use % phi).

    g, x, y = extended_euclidean(e, phi)
    if g != 1:
        raise ValueError("Inverse does not exist")
    
    return x % phi


# ======================================================================
#  SECTION 2 :  RSA Key-Pair Construction
# ======================================================================


class RSAKeyPair:
    """Holds every component of an RSA key pair.

    Attributes after construction
    -----------------------------
    p, q        : int   — the two secret primes
    n           : int   — modulus  (p * q)
    phi         : int   — Euler's totient  (p-1)(q-1)
    e           : int   — public exponent
    d           : int   — private exponent
    """

    def __init__(self, p, q):
        # TODO — compute and store: self.p, self.q, self.n, self.phi, self.e, self.d
        #   verify p != q
        if(q == p):
            raise ValueError("q cannot equal to each other")
        
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        

        #   Loop until you find e such that gcd(e, phi) == 1.
        e = 2
        while True:
            g, _, _ = extended_euclidean(e, self.phi)

            if(g == 1):
                break

            e += 1

        self.e = e

        #   compute d 
        self.d = find_modular_inverse(self.e, self.phi)


    def public(self) -> tuple[int, int]:
        """Return the public key."""
        # TODO: return the public key
        return (self.e, self.n)

    def private(self) -> tuple[int, int]:
        """Return the private key."""
        # TODO: return the private key
        return (self.d, self.n)

    def check_fundamental_property(self, m) -> bool:
        """Verify  m^(e·d) mod n == m  for a given m < n.
        """
        # TODO Hint: use pow() for modular exponentiation.
        return pow(m, self.e * self.d, self.n) == m


# ======================================================================
#  SECTION 3 :  Hashing (the only place hashlib is allowed)
# ======================================================================


def hash_message(message: str, n: int) -> int:
    """Hash a message string into an integer in [0, n).
    """
    digest = hashlib.sha256(message.encode()).hexdigest()
    # TODO: convert hex digest to int, return int % n
    return int(digest, 16) % n


# ======================================================================
#  SECTION 4 :  RSA Signing & Verification
# ======================================================================


def sign_raw(m: int, private_key: tuple[int, int]) -> int:
    """Produce a raw RSA signature on a numeric value.

    Sign using the RSA private key.
    """
    # TODO: Hint: use pow() for modular exponentiation.
    return pow(m, private_key[0], private_key[1])


def verify_raw(m: int, signature: int, public_key: tuple[int, int]) -> bool:
    """Verify a raw RSA signature on a numeric message m.

    Check using public_key. Returns True if valid, False otherwise.
    """
    # TODO: Hint: use pow() for modular exponentiation.
    return m == pow(signature, public_key[0], public_key[1])


def sign_message(message: str, private_key: tuple[int, int]) -> int:
    """Hash-then-sign: hash the message to get m, then sign m.
    """
    # TODO: hash the message, then sign it
    m = hash_message(message, private_key[1])
    return sign_raw(m, private_key)


def verify_message(message: str, signature: int, public_key: tuple[int, int]) -> bool:
    """Verify a hash-then-sign RSA signature.

    Returns True if valid, False otherwise.
    """
    # TODO — hash the message, then verify it
    m = hash_message(message, public_key[1])
    return verify_raw(m, signature, public_key)


# ======================================================================
#  SECTION 5 :  Forgery Detection Experiment
# ======================================================================


def forgery_experiment(kp: RSAKeyPair) -> dict:
    """Demonstrate that altering even one character invalidates the signature.

    Returns a dict:
        {
            "original":  str,       # the original message
            "tampered":  str,       # the tampered message
            "signature": int,       # signature on the original
            "original_valid":  bool,  # should be True
            "tampered_valid":  bool,  # should be False
        }
    """
    original  = "Transfer $100 to Alice"
    tampered  = "Transfer $900 to Alice"

    private_key = kp.private()
    public_key = kp.public()

    # TODO:
    #   Sign the original message.
    signed_m = sign_message(original, private_key)
    #   Verify the signature against BOTH messages.
    original_valid = verify_message(original, signed_m, public_key)
    tampered_valid = verify_message(tampered, signed_m, public_key) 
    #   Return the dict described above.
    return {
            "original":  original,       # the original message
            "tampered":  tampered,       # the tampered message
            "signature": signed_m,       # signature on the original
            "original_valid":  original_valid,  # should be True
            "tampered_valid":  tampered_valid,  # should be False
        }



# ======================================================================
#  SECTION 6 :  Demo Driver
# ======================================================================


def main():
    # --- key generation ---
    print("\n>> Generating RSA key pair ...")
    # Pick p and q from PRIME_LIST, and they must be distinct.
    kp = RSAKeyPair(251, 257)

    # TODO: check fundamental property
    test_m = 77
    ok = kp.check_fundamental_property(test_m)
    print(f"\n>> Fundamental property for M={test_m}?  {ok}")
    assert ok

    private_key = kp.private()
    public_key = kp.public()
    # --- raw sign / verify ---
    print("\n>> Raw signature on numeric message ...")
    raw_msg = 123
    # TODO: sign the raw message
    sig = sign_raw(raw_msg, private_key)
    print(f"   message  = {raw_msg}")
    print(f"   signature = {sig}")

    # TODO: verify the signature
    v = verify_raw(raw_msg, sig, public_key)
    print(f"   valid?    = {v}")
    assert v

    # --- hash-then-sign on text ---
    print("\n>> Hash-then-sign on text message ...")
    text = "Cryptography is fun"
    # TODO: sign the text message
    sig2 = sign_message(text, private_key)
    print(f'   message   = "{text}"')
    print(f"   signature = {sig2}")

    # TODO: verify the signature
    v2 = verify_message(text, sig2, public_key)
    print(f"   valid?    = {v2}")
    assert v2

    # --- forgery experiment ---
    print("\n>> Forgery detection experiment ...")
    result = forgery_experiment(kp)
    print(f'   original : "{result["original"]}"  → valid={result["original_valid"]}')
    print(f'   tampered : "{result["tampered"]}"  → valid={result["tampered_valid"]}')
    assert result["original_valid"] is True
    assert result["tampered_valid"] is False


if __name__ == "__main__":
    main()
