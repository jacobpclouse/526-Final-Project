a = 0b1010  # binary representation of 10
b = 0b1100  # binary representation of 12

c = a ^ b   # XOR operation

print(bin(c))  # prints 0b0110, which is 6 in decimal


output = c ^ b

print(f"ouput = {output} and a = {a}")