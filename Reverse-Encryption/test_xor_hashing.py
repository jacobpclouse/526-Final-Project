import hashlib

# create a hash object using the SHA-256 hash function
hash_one = hashlib.sha256(b'Hello, world!')
hash_two = hashlib.sha256(b'thisisreallif')

# get the binary digest of the hashed message
hex_digest1 = hash_one.hexdigest()
hex_digest2 = hash_two.hexdigest()

print(hex_digest1)
print(hex_digest2)



xored = ""
for i in range(len(hex_digest1)):
    xored += chr(ord(hex_digest1[i]) ^ ord(hex_digest2[i]))
print("   ")
print(xored)  
print("   ")

output = ""
for i in range(len(xored)):
    output += chr(ord(xored[i]) ^ ord(hex_digest1[i]))

print(f"output = {output} and hex2 = {hex_digest2}")

if output == hex_digest2:
    print("output is equal to hex digest 2")
else:
    print('not equal')