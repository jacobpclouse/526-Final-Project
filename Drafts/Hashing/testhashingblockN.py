import hashlib

# we can use this to take the n input and act as if it is a bit of extra 'salt'

n = input("Give me a number: ")
# n = 16
h0 = hashlib.sha256((str(n).encode())).hexdigest()

print(f"h0: {h0}")
print('\n')
print(f"h0 len: {len(h0)}")