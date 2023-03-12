import hashlib
import ecdsa

'''

DO NOT USE THIS, IT DOES NOT WORK!!!!!!!!!!
ONLY useful for concepts

'''


# Define the elliptic curve and the generator point
secp256k1_curve = ecdsa.curves.SECP256k1
generator_point = secp256k1_curve.generator

# Generate a random private key
private_key = ecdsa.util.randrange(1, secp256k1_curve.order)

# Compute the public key by multiplying the generator point by the private key
public_key_point = private_key * generator_point
public_key = public_key_point.to_string()

# Hash the public key with SHA-256 and then with RIPEMD-160
public_key_hash = hashlib.sha256(public_key).digest()
ripemd160_hash = hashlib.new('ripemd160', public_key_hash).digest()

# Add the network byte to the RIPEMD-160 hash
network_byte = b'\x00' # for Bitcoin mainnet
extended_ripemd160_hash = network_byte + ripemd160_hash

# Double hash the extended RIPEMD-160 hash with SHA-256
hash1 = hashlib.sha256(extended_ripemd160_hash).digest()
hash2 = hashlib.sha256(hash1).digest()

# Take the first 4 bytes of the double hash as the checksum
checksum = hash2[:4]

# Add the checksum to the extended RIPEMD-160 hash to create the address
address = extended_ripemd160_hash + checksum

# Encode the address in base58
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base58_chars = []
value = int.from_bytes(address, byteorder='big')
while value > 0:
    value, remainder = divmod(value, 58)
    base58_chars.append(alphabet[remainder])
base58_chars.reverse()
base58_address = ''.join(base58_chars)

print("Private key: {}".format(hex(private_key)))
print("Public key: {}".format(public_key.hex()))
print("Address: {}".format(base58_address))
