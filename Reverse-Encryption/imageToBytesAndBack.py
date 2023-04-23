from PIL import Image

# Open image file
image = Image.open('4041x4041square.jpg')

# Get image size
width, height = image.size
print(f"Image size: {width} x {height}")

# Convert image to bytes
image_bytes = image.tobytes()
print(f"Image bytes: {len(image_bytes)} bytes")

# Convert bytes back to image
expected_length = width * height * 3  # 3 bytes per pixel in RGB mode
if len(image_bytes) == expected_length:
    reconstructed_image = Image.frombytes(mode='RGB', size=(width, height), data=image_bytes)
    reconstructed_image.show()
else:
    print("Error: not enough image data.")