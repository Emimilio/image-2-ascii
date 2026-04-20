
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageFilter, ImageChops
from scipy.ndimage import convolve

CHAR_MAP = np.array([" ", ".", "i", "c", "o", "P", "O", "?", "@"])
EDGE_MAP = np.array(["_", "/", "|", "\\", "_"])
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

    edge_chars = np.array(["|", "\\", "-", "/", "|", "\\", "-", "/"])
    indices = ((teta + 0.0625) * 8 % 8).astype(int)
    edge_matrix = edge_chars[indices]

    threshold = 10
    edge_matrix[magnitude < threshold] = " "

    return edge_matrix


def get_image_high_freq(image: Image) -> Image:
    """
    Image substracts the low frequencies by using a gaussian 
    filter to retain the high frequencies
    """
    gray_image = image.convert("L")
    blurred = gray_image.filter(ImageFilter.GaussianBlur(radius=2))
    return ImageChops.difference(gray_image, blurred)
