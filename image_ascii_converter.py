
import numpy as np
import numpy.typing as npt
from PIL import Image 
from scipy.ndimage import convolve
from skimage.filters import gaussian
from skimage import feature

CHAR_MAP = np.array([" ", ".", "i", "c", "o", "P", "O", "?", "@"])
EDGE_MAP = np.array(["|", "\\", "-", "/", "|", "\\", "-", "/"])
IMPROVED_EDGE_MAP = np.array(["▏", "╲", "_", "╱", "▕", "╲", "‾", "╱"])
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

def normalize_image(array: npt.NDArray) -> npt.NDArray:
    if array.max() > 1.0:
        return array.astype(float) / 255.0

    return array

def scale_image_to_255(array: npt.NDArray) -> npt.NDArray:
    return (array * 255).astype(np.uint8)

def resize_image_np_array(image_array: npt.NDArray) -> npt.NDArray:
    array = scale_image_to_255(image_array)
    im = Image.fromarray(array)
    return resize_image(im)

def resize_image(image: Image) -> Image:
    width, height = image.size
    new_width, new_height = (width // 8, height // int(8 * 1.2))

    return image.resize((new_width, new_height), Image.LANCZOS)

def map_pixel_to_ascii(image: Image) -> npt.NDArray:
    image_hsv = image.convert("HSV")
    v_channel = np.array(image_hsv)[:, :, V_IDX]

    char_idxs = (v_channel / 255 * (len(CHAR_MAP) - 1)).astype(int)
    ascii_matrix = CHAR_MAP[char_idxs]

    return ascii_matrix

def detect_edges(image: Image) -> npt.NDArray:
    gray_image = normalize_image(np.array(image.convert("L")))
    gx, gy, magnitude = apply_sobel_filter(gray_image)

    teta = (np.atan2(gy, gx) / np.pi) * 0.5 + 0.5

    indices = ((teta + 0.0625) * len(EDGE_MAP) % len(EDGE_MAP)).astype(int)
    edge_matrix = EDGE_MAP[indices]

    max_mag = magnitude.max()
    threshold = max_mag * 0.0
    edge_matrix[magnitude < threshold] = " "

    return edge_matrix

def apply_sobel_filter(image: npt.NDArray) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
    gx = convolve(image, GX_SOBEL)
    gy = convolve(image, GY_SOBEL)
    magnitude = np.hypot(gx, gy)
    return gx, gy, magnitude

def get_difference_of_gaussian(image: Image, sigma=1) -> Image:
    im = normalize_image(np.array(image.convert("L")))

    g_1 = gaussian(im, sigma=sigma)
    g_2 = gaussian(im, sigma=1.6 * sigma)

    diff = g_1 - g_2

    diff_min, diff_max = diff.min(), diff.max()
    if diff_max - diff_min > 0:
        diff_normalized = (diff - diff_min) / (diff_max - diff_min)
    else:
        diff_normalized = diff

    threshold = 0.6
    threshold_im = np.where(diff_normalized > threshold, 1.0, 0.0)
    DoG = scale_image_to_255(threshold_im)
    return Image.fromarray(DoG)


def convert_image_to_ascii(image: Image) -> tuple[npt.NDArray, npt.NDArray]:
    image = image.convert("RGB")
    image_resized = resize_image(image)
    image_rgb = image_resized.convert("RGB")
    gray_image = image_resized.convert("L")

    im = feature.canny(np.array(gray_image), sigma=1)
    Image.fromarray(im).show()
    edge_matrix = detect_edges(image_resized)

    edge_matrix = np.where(im, edge_matrix, " ")

    ascii_matrix = map_pixel_to_ascii(image_resized)
    ascii_image = np.where(edge_matrix == " ", ascii_matrix, edge_matrix)

    return ascii_image, np.array(image_resized)
