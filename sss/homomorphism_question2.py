from PIL import Image

import sss.sss_question2
import numpy as np

from sss import sss_question2

n = 3
k = 2


# Step 1: Downscale operation
def downscale(path='image.bmp', name='downscaled_image.bmp'):
    # Load the input image
    img = Image.open(path).convert('L')

    # Get the dimensions of the input image
    width, height = img.size

    # Calculate the dimensions of the downscaled image
    downscaled_width = width // 2
    downscaled_height = height // 2

    # Create a new array to hold the downscaled image
    downscaled_image = np.zeros((downscaled_height, downscaled_width), dtype=np.uint8)
    pixels = []
    # Loop through each pixel in the downscaled image
    for y in range(downscaled_height):
        for x in range(downscaled_width):
            # Compute the average value of the four pixels in the input image
            pixels.append(img.getpixel((2 * x, 2 * y)))
            pixels.append(img.getpixel((2 * x + 1, 2 * y)))
            pixels.append(img.getpixel((2 * x, 2 * y + 1)))
            pixels.append(img.getpixel((2 * x + 1, 2 * y + 1)))

            # Set the pixel value in the downscaled image
            downscaled_image[y, x] = sum(pixels)

    # Create a PIL Image object from the downscaled image array
    downscaled_img = Image.fromarray(downscaled_image)

    # Save the downscaled image to a file
    downscaled_img.save(name)

    img = np.asarray(img)
    return img.flatten(), downscaled_img, img.shape, downscaled_width, downscaled_height


# Step 2: Create 3 shares (denoted by I1, I2, I3) of I using the SSS scheme.
def generate_shares(img, i_0_shape, n=n):
    return sss_question2.generate_shares(img, 'grayscale', i_0_shape, n=n)


# Step 3: Perform the downscale method on all the three shares and obtain the downscaled shares
# (denoted by Is1, Is2, Is3).
def downscale_shares(share_paths):
    shares = []
    share_names = []
    img_list = []
    for i in range(len(share_paths)):
        name = f'share{i}_downscaled.bmp'
        result = downscale(share_paths[i], name)
        share = list(result[0])
        shares.append(share)
        share_names.append(name)
        img_list.append(result[1])
    return np.array(shares), share_names


# Step 4: Pick any 2 downscaled shares, i.e., from Is1, Is2, Is3, and reconstruct the downscaled plaintext
# image (denoted by Is).
def reconstruct_downscaled(shares, shape, k):
    print("reconstructing...")
    # shares = np.array([(1, s1), (2, s2)])
    result = sss_question2.reconstruct(shares, shape, k=k, name="reconstructed_img.bmp")
    reconstructed_image = result[0]
    data = result[1]
    return data, reconstructed_image


# Step 5: Compute the mean average error between the two images, Io and Is, using the following
# equation:
def compute_mae(pixels_0, pixels_s, w, h):
    mae = 0
    for i in range(w * h):
        mae += abs(pixels_0[i] - pixels_s[i])
    mae /= w * h
    return mae


if __name__ == '__main__':
    i, i_shape = sss_question2.read_grayscale_pixels('image.bmp')
    # step 1
    i_0, downscaled_img, i_0_shape, i_0_w, i_0_h = downscale()

    # step 2
    shares, share_paths = generate_shares(i, i_0_shape)

    # step 3
    # share_paths = ["share_grayscale_1.bmp", "share_grayscale_2.bmp", "share_grayscale_3.bmp"]
    downscaled_shares = downscale_shares(share_paths)[0]

    # step 4
    reconstructed_image = reconstruct_downscaled(downscaled_shares[0:k, :], i_shape, k)[0]

    # step 5
    mae = compute_mae(i_0, reconstructed_image.flatten(), i_0_w, i_0_h)
    print('MAE:', mae)
