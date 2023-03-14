from Crypto.PublicKey import ECC

# Generate a private key
private_key = ECC.generate(curve='P-256')
print(f"private key: {private_key}")

# Get the public key
public_key = private_key.public_key()
print(f"public key: {public_key}")

# Generate a random scalar to multiply with the private key
scalar = ECC.generate(curve='P-256')

# Multiply the public key with the scalar
result_public_key = public_key.pointQ * scalar.d

# Multiply the private key with the scalar
result_private_key = private_key.d * scalar.d

print("Result public key:", result_public_key)
print("Result private key:", result_private_key)
