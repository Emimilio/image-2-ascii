
import numpy as np
import numpy.typing as npt
from PIL import Image 
from skimage import feature
import utils


def convert_image_to_ascii(image: Image, ) -> tuple[npt.NDArray, npt.NDArray]:
    image = image.convert("RGB")
    image_resized = utils.resize_image(image)
    gray_image = utils.normalize_image(np.array(image_resized.convert("L")))

    canny_edge_mask = feature.canny(gray_image, sigma=1)
    edge_matrix = utils.detect_edges(gray_image)
    edge_matrix = np.where(canny_edge_mask, edge_matrix, " ")

    ascii_matrix = utils.map_pixel_to_ascii(image_resized)
    ascii_image = np.where(edge_matrix == " ", ascii_matrix, edge_matrix)

    return ascii_image, np.array(image_resized)
