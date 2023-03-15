# https://www.geeksforgeeks.org/hashlib-module-in-python/

# importing hashlib for getting sha256() hash function
import hashlib


# A string that has been stored as a byte stream
# (due to the prefix b)
string = b"My name is apple and I am a vegetable?"
string2 = b'No I am not a vegetable, I am a meat!'

# Initializing the sha256() method
sha256 = hashlib.sha256()


# Passing the byte stream as an argument
sha256.update(string)
string_hash = sha256.hexdigest()

# Round 2
sha256.update(string2)
string_hash2 = sha256.hexdigest()


# sha256.hexdigest() hashes all the input data
# passed to the sha256() via sha256.update()
# Acts as a finalize method, after which all
# the input data gets hashed
# hexdigest() hashes the data, and returns
# the output in hexadecimal format
# string_hash = sha256.hexdigest()


print(f"Hash 1:{string_hash}")
print(f"Hash 2:{string_hash2}")

