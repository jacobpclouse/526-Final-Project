import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.util import string_to_number

# Generate a private key
private_key = ecdsa.SigningKey.generate(curve=SECP256k1)

# Get the corresponding public key
public_key = private_key.get_verifying_key()

# Print the private and public keys as hex-encoded strings
print("Private key: ", private_key.to_string().hex())
print("Public key: ", public_key.to_string().hex())

# Convert the public and private keys to integers
private_key_int = string_to_number(private_key.to_string())
public_key_int = string_to_number(public_key.to_string())

# Multiply the public key and the private key
result = private_key_int * public_key_int

# Print the result as a hex-encoded string
print("Result: ", hex(result))
