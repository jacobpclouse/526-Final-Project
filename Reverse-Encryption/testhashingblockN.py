import hashlib

n = 16
h0 = hashlib.sha256(n.encode()).hexdigest()


print(len(n))