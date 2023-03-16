# this is used to store byte arrays and then get the data back out

import pickle

# sample data
byte_array = [
    b'\x19\xc9\xcb\xbb8\xf9\x9a3\xba0\xa3\x0f\x84H\x01\x84\xa7%\xa2\x88\xb5\x98\x1e\xdb|\xf1\x04\x19~\x05\x12\xc6',
    b'd\xaf\x8amg=@\x9b\xb6h\x83\xbf\x80\xd3~q\x851\xe8\xcf\xaa|t\x0c\xd1\xb0H\xc6\xe8 v\x9a',
    b'M\xe6o\x9d\x961\xa8;\x1b\xc29\xf75\xc7O\x08\xb4>\xcc\x94\x19\xe7=>\x1a\xe2N5\xbcey\xdd'
]

# Open the file in binary mode and use pickle to serialize the byte array to the file
with open('byte_array.pickle', 'wb') as f:
    pickle.dump(byte_array, f)

# Read the byte array back from the file
with open('byte_array.pickle', 'rb') as f:
    loaded_byte_array = pickle.load(f)

# Print the loaded byte array
print(loaded_byte_array)
