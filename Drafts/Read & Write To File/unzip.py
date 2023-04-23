import zipfile

# Name of the zip file to extract
zip_file_name = "newZip.zip"

# Create a ZipFile object with the name of the zip file and mode 'r' for read
with zipfile.ZipFile(zip_file_name, mode='r') as zip_obj:
    
    # Print a list of all files in the zip file
    print("Files in zip file:")
    for file_name in zip_obj.namelist():
        print(f"- {file_name}")
    
    # Extract all files to the current working directory
    zip_obj.extractall()
    
# The extracted files will be saved in the same directory as this script
