# ── pow() — Modular Exponentiation ──
# pow(base, exp, mod) computes (base ** exp) % mod efficiently.
# It uses square-and-multiply internally, so it's fast even for large numbers.
#
# Examples:
pow(2, 10, 1000)   # => 1024 % 1000 = 24
pow(88, 7, 187)    # => 11
pow(11, 23, 187)   # => 88


# ── dict — Creating Dictionaries ──
person = {
    "name": "Alice",
    "age": 25,
    "active": True,
}

# Accessing values
print(person["name"])      # "Alice"

# Adding / updating a key
person["email"] = "alice@example.com"

# Storing a tuple as a value
person["coordinates"] = (30.0, 31.2)

# Building a dict step by step
result = {}
result["p"] = 17
result["q"] = 11
result["n"] = result["p"] * result["q"]
result["public_key"] = (7, result["n"])

