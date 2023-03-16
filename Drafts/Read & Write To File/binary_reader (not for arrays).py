# --- Function that reads data from a BINARY file, prints it ---
def read_data_from_file(input_file_name):
    with open(f"{input_file_name}.bin", 'rb') as f:
        data = f.read()
        # print(data)
        return data


# useThisFileName = input("Give me the input name without the ending: ")
useThisFileName = 'Data_encryption_normal__2023-03-16_14_25_36-947270'
readIn = read_data_from_file(useThisFileName)
print(f"Returned Data: {readIn}")