import base64
from PIL import Image

# Open image file
with open('4041x4041square.jpg', 'rb') as image_file:
    # Read image data
    image_data = image_file.read()
    
    # Encode image data using Base64
    encoded_image = base64.b64encode(image_data)
    
    # Convert byte string to string
    encoded_image_str = encoded_image.decode('utf-8')
    
    # Print encoded image string
    print(encoded_image_str)
