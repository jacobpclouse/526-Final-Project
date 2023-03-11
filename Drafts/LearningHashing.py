# https://www.geeksforgeeks.org/hashlib-module-in-python/

# Trying to learn Hashlib

# importing sys for getting commandline arguments
import sys

# importing hashlib for getting sha256() hash function
import hashlib


def hashfile(file):

	# A arbitrary (but fixed) buffer size
	# 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

	# Initializing the sha256() method
    sha256 = hashlib.sha256()

	# Opening the file provided as the first
	# commandline argument
	# with open("test.txt", 'rb') as f:
    with open(sys.argv[1], 'rb') as f:
        while True:
			# reading data = BUF_SIZE from the
			# file and saving it in a variable
            data = f.read(BUF_SIZE)

			# True if eof = 1
            if not data:
                break

			# Passing that data to that sh256 hash
			# function (updating the function with that data)
            sha256.update(data)

	# sha256.hexdigest() hashes all the input data passed
	# to the sha256() via sha256.update()
	# Acts as a finalize method, after which
	# all the input data gets hashed
	# hexdigest() hashes the data, and returns
	# the output in hexadecimal format
    return sha256.hexdigest()


# Calling hashfile() function to obtain hash of the file
# and saving the result in a variable
file_hash = hashfile(sys.argv[1])

print(f"Hash:{file_hash}")
