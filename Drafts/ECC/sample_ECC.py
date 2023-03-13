from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import ECC
from tinyec import registry

# Generate a private key
private_key = ECC.generate(curve='P-256')

# Get the public key
public_key = private_key.public_key()

# Convert the private key to an integer
d = private_key.d

# Get the curve parameters from the public key
curve_str = public_key.curve.curve
curve = registry.get_curve(curve_str)

# Compute the scalar multiplication of the public key by the private key
Q = (public_key.pointQ.x, public_key.pointQ.y)
n = curve.field.n
k = d % n
Q_prime = curve.multiply(Q, k)

# Print the result in hexadecimal format
print("Result: ", Q_prime)
print("Result (hex): ", hex(Q_prime[0])[2:], hex(Q_prime[1])[2:])
