
# Step 4: Hash e using H1 as initialization vector and store in H1
# H1 = hashlib.sha256(e, H1).digest() #ERRORING - how do we hash two variables? ****
# Concatenate e and H1 before hashing
data_to_hash = e + H1
H1 = hashlib.sha256(data_to_hash).digest()
# H1_temp = generate_hash3(e, H1)
# H1 = H1_temp.encode('utf-8')
if chooseDebugMode == 'YES':
    print(f"data_to_hash: {data_to_hash}")
    print(f"NEW H1: {H1}")

# # --- Function to to hash two arguments - BYTES OBJECT ONLY ---
def generate_hash3(secret, param_str):
    dk = hashlib.sha256()
    s = secret + param_str  # concatenate strings, then hash
# #   dk.update(s.encode('utf-8'))
    dk.update(s)
    return dk.hexdigest()


#did not work!!