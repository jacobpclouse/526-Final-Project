import hashlib

# create a hash object using the SHA-256 hash function
hash_object = hashlib.sha256(b'Hello, world!')

# get the binary digest of the hashed message
binary_digest = hash_object.digest()
hex_digest = hash_object.hexdigest()

print(binary_digest)
print(hex_digest)


