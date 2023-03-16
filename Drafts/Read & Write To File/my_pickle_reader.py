# this is used to store byte arrays and then get the data back out

import pickle

userPickleFile = 'encryption_normal'

# Read the byte array back from the file
with open(f'{userPickleFile}.pickle', 'rb') as f:
    loaded_byte_array = pickle.load(f)


encrypt_message_hex = loaded_byte_array.hex() # this works, it brings it back to the original data in hex form
# Print the loaded byte array
print(loaded_byte_array)
print("\n")
print(f"Final Read: {encrypt_message_hex}")