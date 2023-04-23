import pickle

inputPickle = input("input filename: ")
# Open the pickle file in read mode
with open(inputPickle, 'rb') as f:
    # Load the data from the pickle file
    data = pickle.load(f)
    
    # Print each line in the data
    for line in data:
        print(line)