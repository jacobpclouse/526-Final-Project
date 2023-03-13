import ecdsa

# Generate an elliptic curve key pair
sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
vk = sk.get_verifying_key()

# Convert the keys to bytes format
sk_bytes = sk.to_string()
vk_bytes = vk.to_string()

# Convert the bytes to integers
sk_int = int.from_bytes(sk_bytes, byteorder="big")
vk_int = int.from_bytes(vk_bytes, byteorder="big")

# Define the scalar multiplier
scalar = 123456789

# Perform scalar multiplication on the private and public keys
sk_int_new = (sk_int * scalar) % sk.curve.generator.order()
vk_int_new = ecdsa.ecdsa.Public_key(sk.curve.generator, sk.curve.generator * sk_int_new).point.x()

# Convert the integers back to bytes format
sk_bytes_new = sk_int_new.to_bytes((sk_int_new.bit_length() + 7) // 8, byteorder="big")
vk_bytes_new = vk_int_new.to_bytes((vk_int_new.bit_length() + 7) // 8, byteorder="big")

# Convert the bytes back to elliptic curve keys
sk_new = ecdsa.SigningKey.from_string(sk_bytes_new, curve=ecdsa.SECP256k1)
vk_new = ecdsa.VerifyingKey.from_string(vk_bytes_new, curve=ecdsa.SECP256k1)

# Print the original and new keys
print("Original private key:", sk.to_string().hex())
print("Original public key:", vk.to_string().hex())
print("New private key:", sk_new.to_string().hex())
print("New public key:", vk_new.to_string().hex())
