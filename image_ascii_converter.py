
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageFilter, ImageChops
from scipy.ndimage import convolve, gaussian_filter
from skimage.filters import gaussian

CHAR_MAP = np.array([" ", ".", "i", "c", "o", "P", "O", "?", "@"])
EDGE_MAP = np.array(["|", "\\", "-", "/", "|", "\\", "-", "/"])
V_IDX = 2

GX_SOBEL = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
]).astype(float)

GY_SOBEL = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1],
]).astype(float)

def resize_image(image: Image) -> Image:
    width, height = image.size
    new_width, new_height = (width // 8, height // 8)

    return image.resize((new_width, new_height), Image.LANCZOS)

def convert_image_to_ascii(image: Image) -> npt.NDArray:
    image_hsv = image.convert("HSV")
    v_channel = np.array(image_hsv)[:, :, V_IDX]

    char_idxs = (v_channel / 255 * (len(CHAR_MAP) - 1)).astype(int)
    ascii_matrix = CHAR_MAP[char_idxs]

    return ascii_matrix


def detect_edges(image: Image) -> npt.NDArray:
    gray_image = np.array(image.convert("L")).astype(float) # TEMPORARY
    gx = convolve(gray_image, GX_SOBEL)
    gy = convolve(gray_image, GY_SOBEL)
    magnitude = np.sqrt(gx**2 + gy**2)

    teta = (np.atan2(gy, gx) / np.pi) * 0.5 + 0.5

    indices = ((teta + 0.0625) * len(EDGE_MAP) % len(EDGE_MAP)).astype(int)
    edge_matrix = EDGE_MAP[indices]

    max_mag = magnitude.max()
    threshold = max_mag * 0.1
    edge_matrix[magnitude < threshold] = " "

    return edge_matrix

def get_difference_of_gaussian(image: Image, sigma=1) -> Image:
    im = np.array(image.convert("L")).astype(float) / 255.0
    
    g_1 = gaussian(im, sigma=sigma)
    g_2 = gaussian(im, sigma=1.6 * sigma) 

    diff = g_1 - g_2

    diff_min, diff_max = diff.min(), diff.max()
    if diff_max - diff_min > 0:
        diff_normalized = (diff - diff_min) / (diff_max - diff_min)
    else:
        diff_normalized = diff

    threshold_im = np.where(diff_normalized > 0.6, 1.0, 0.0)
    DoG = (threshold_im * 255).astype(np.uint8)

    return Image.fromarray(DoG)
