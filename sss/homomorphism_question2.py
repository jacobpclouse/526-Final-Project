from PIL import Image

import sss_question2
import numpy as np

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
    return img.flatten(), img.shape, downscaled_width, downscaled_height


# Step 2: Create 3 shares (denoted by I1, I2, I3) of I using the SSS scheme.
def generate_shares(img):
    return sss_question2.generate_shares(img, 'grayscale', i_0_shape, n=n)


# Step 3: Perform the downscale method on all the three shares and obtain the downscaled shares
# (denoted by Is1, Is2, Is3).
def downscale_shares(share_paths):
    share1 = downscale(share_paths[0], 'share1_downscaled.bmp')[0]
    share2 = downscale(share_paths[1], 'share2_downscaled.bmp')[0]
    share3 = downscale(share_paths[2], 'share3_downscaled.bmp')[0]
    return np.array([list(share1), list(share2), list(share3)])


# Step 4: Pick any 2 downscaled shares, i.e., from Is1, Is2, Is3, and reconstruct the downscaled plaintext
# image (denoted by Is).
def reconstruct_downscaled(shares, shape):
    # shares = np.array([(1, s1), (2, s2)])
    data = sss_question2.reconstruct(shares, shape, k=k, name="reconstructed_downscaled.bmp")[1]
    return data


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
    i_0, i_0_shape, i_0_w, i_0_h = downscale()

    # step 2
    shares = generate_shares(i)

    # step 3
    share_paths = ["share_grayscale_1.bmp", "share_grayscale_2.bmp", "share_grayscale_3.bmp"]
    downscaled_shares = downscale_shares(share_paths)

    # step 4
    reconstructed_image = reconstruct_downscaled(downscaled_shares[0:k, :], i_shape)

    # step 5
    mae = compute_mae(i_0, reconstructed_image.flatten(), i_0_w, i_0_h)
    print('MAE:', mae)
