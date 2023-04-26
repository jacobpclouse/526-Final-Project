with open('testphoto.png', 'rb') as image_file:
    bytes_file = image_file.read()

with open('example_bytes_file.cipher', 'wb') as bytes_file_output:
    bytes_file_output.write(bytes_file)