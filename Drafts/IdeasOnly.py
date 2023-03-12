# https://stackoverflow.com/questions/4273466/reversible-hash-function
import hashlib


def reversible_hash(data):
    # Convert data to bytes
    data_bytes = bytes(data, 'utf-8')

    # Create a hash object using the SHA256 algorithm
    hash_obj = hashlib.sha256(data_bytes)

    # Get the hexadecimal representation of the hash
    hex_digest = hash_obj.hexdigest()

    # Return the hexadecimal representation of the hash as bytes
    return bytes.fromhex(hex_digest)


def reverse_hash(hash_bytes):
    # Create a hash object using the SHA256 algorithm
    hash_obj = hashlib.sha256()

    # Update the hash object with the hash bytes
    hash_obj.update(hash_bytes)

    # Get the original data as bytes
    data_bytes = hash_obj.digest()

    # Return the original data as bytes
    return data_bytes

'''
def reverse_hash(hash_bytes):
    # Create a hash object using the SHA256 algorithm
    hash_obj = hashlib.sha256()

    # Update the hash object with the hash bytes
    hash_obj.update(hash_bytes)

    # Get the original data as bytes
    data_bytes = hash_obj.digest()

    # Return the original data as a string
    return data_bytes.decode('utf-8')
'''
'''
hashed_bytes = b'1_[\xdbv\xd0x\xc4;\x8a\xc0\x06NJ\x01da+\x1f\xcew\xc8i4[\xfc\x94\xc7X\x94\xed\xd3'
original_data_bytes = reverse_hash(hashed_bytes)
print(original_data_bytes)  # b'Hello, world!'
'''


data = 'Hello, world!'
hashed_bytes = reversible_hash(data)
print(hashed_bytes)  # b'\xf4\x1d\x84\x87\xee\x4e\xee\x9c\x24\xe9\x37\x70\x31\xfa\x52\xdc\x10\x48\x81\x15\x99\x1d\xc9\x32\x7b\x9d\x49\x17\x7b\x3b\x4b'

original_data = reverse_hash(hashed_bytes)
print(original_data)  # Hello, world!