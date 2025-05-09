#! /usr/bin/env python3
import math
import random
# Create a random-number generator.
r = random.Random()
# We need to find a prime modulus.
def find_prime(min_val, max_val):
    # We can define functions within the scope of other functions.
    def is_prime(p):
        if 0 == p % 2:
            return False
        for f in range(3, int(math.sqrt(p))+1, 2):
            if 0 == p % f:
                return False
        return True
        # Loop until we've found a prime.
    while True:
        v = r.randint(min_val,max_val)
        print(v)
        if is_prime(v):
            return(v)
        
def make_key():
    p = find_prime(16,64)
    while True:
        q = find_prime(16,64)
        if q != p:
            break
    n = p * q
    phi = (p-1) * (q-1)
    e = 3
    d = None

    for x in range(phi):
        if 1 == (e*x) % phi:
            d = x
        break
    return (p,q,n,e,phi,d)

while True:
    p,q,n,e,phi,d = make_key()
    if d is not None:
        break

print(f'Public key: {n}, {e}')
print(f'Private key: {p}, {q}, {phi}, {d}')
# Alice is choosing this.
key = r.randint(0,255)
# Alice can now encrypt key for Bob and send it to him.
cipher = key ** e % n
# Bob can decrypt it, and now they share a key for an XOR block cipher.
plain = cipher ** d % n
assert key == plain
c = 45 ^ key
m = c ^ plain
assert m == 45