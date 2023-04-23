import zipfile
import os

# -- Function that takes zip name and then an array of files to zip
def zip_files(zip_name, files_to_zip):
    """
    Given a name and a list of file paths, this function creates a new
    zip file with the given name and adds all the specified files to it.
    """
    with zipfile.ZipFile(zip_name, 'w') as zip_file:
        # Add each file to the zip file
        for file_path in files_to_zip:
            # Add the file to the zip file with its original name
            zip_file.write(file_path, arcname=file_path.split('/')[-1])
            
    print(f"All files zipped into {zip_name}")

testPath = 'test'
name = 'newZip.zip'
# files = ['test_encryption_numpy_array.npy','the_enck_val.bin']
files = [os.path.join(testPath,'test_encryption_numpy_array.npy'),os.path.join(testPath,'the_enck_val.bin')]

zip_files(name,files)