
import numpy as np
import numpy.typing as npt
from PIL import Image
from scipy.ndimage import convolve

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

def resize_image(image: Image) -> Image:
    width, height = image.size
    new_width, new_height = (width // 8, height // int(8 * 1.2))

    return image.resize((new_width, new_height), Image.LANCZOS)

def map_pixel_to_ascii(image: Image, char_map: npt.NDArray=CHAR_MAP) -> npt.NDArray:
    image_hsv = image.convert("HSV")
    v_channel = np.array(image_hsv)[:, :, V_IDX]

    char_idxs = (v_channel / 255 * (len(char_map) - 1)).astype(int)
    ascii_matrix = char_map[char_idxs]

    return ascii_matrix

def detect_edges(gray_image: npt.NDArray, threshold: float=0.0) -> npt.NDArray:
    gx, gy, magnitude = apply_sobel_filter(gray_image)
    teta = (np.atan2(gy, gx) / np.pi) * 0.5 + 0.5

    indices = ((teta + 0.0625) * len(EDGE_MAP) % len(EDGE_MAP)).astype(int)
    edge_matrix = EDGE_MAP[indices]
    edge_matrix[magnitude < threshold] = " "

    return edge_matrix

def apply_sobel_filter(image: npt.NDArray) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
    gx = convolve(image, GX_SOBEL)
    gy = convolve(image, GY_SOBEL)
    magnitude = np.hypot(gx, gy)
    return gx, gy, magnitude
