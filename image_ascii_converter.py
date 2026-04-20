
import numpy as np
import numpy.typing as npt
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
from scipy.ndimage import convolve

CHAR_MAP = np.array([" ", ".", "i", "c", "o", "P", "O", "?", "@"])
EDGE_MAP = np.array(["_", "/", "|", "\\", "_"])
V_IDX = 2

GX_SOBEL = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])

GY_SOBEL = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1],
])

def convert_image_to_ascii(image: Image) -> tuple[npt.NDArray, npt.NDArray]:
    image = image.convert("RGB") # convert to RGB just in case the image is HDR (4 dimensions)
    width, height = image.size
    new_width, new_height = (width // 8, height // 8)

    image = image.resize((new_width, new_height), Image.LANCZOS)
    image_hsv = image.convert("HSV")
    ascii_matrix = np.full((new_height, new_width), " ", dtype=object)

    pixels_rgb = np.array(image)
    pixels_hsv = np.array(image_hsv)
    v_channel = pixels_hsv[:, :, V_IDX]

    char_idxs = (v_channel / 255 * (len(CHAR_MAP) - 1)).astype(int)
    ascii_matrix = CHAR_MAP[char_idxs]

    return ascii_matrix, pixels_rgb


def detect_edges(image: Image) -> npt.NDArray:
    gray_image = np.array(image.convert("L")) # TEMPORARY
    gx = convolve(gray_image, GX_SOBEL)
    gy = convolve(gray_image, GY_SOBEL)
    magnitude = np.sqrt(gx**2 + gy**2)

    teta = (np.atan2(gy, gx) / np.pi) * 0.5 + 0.5

    edge_matrix = np.full(teta.shape, " ", dtype=object)
    # 1. Horizontal: Near 0, 0.5, and 1.0
    # Ranges: [0, 0.0625], [0.4375, 0.5625], [0.9375, 1.0]
    edge_matrix[(teta < 0.0625) | 
                ((teta >= 0.4375) & (teta <= 0.5625)) | 
                (teta > 0.9375)] = "-"

    # 2. Diagonal Forward (/): Near 0.125 and 0.625
    # Ranges: [0.0625, 0.1875], [0.5625, 0.6875]
    edge_matrix[((teta > 0.0625) & (teta < 0.1875)) | 
                ((teta > 0.5625) & (teta < 0.6875))] = "/"

    # 3. Vertical: Near 0.25 and 0.75
    # Ranges: [0.1875, 0.3125], [0.6875, 0.8125]
    edge_matrix[((teta >= 0.1875) & (teta <= 0.3125)) | 
                ((teta >= 0.6875) & (teta <= 0.8125))] = "|"

    # 4. Diagonal Backward (\): Near 0.375 and 0.875
    # Ranges: [0.3125, 0.4375], [0.8125, 0.9375]
    edge_matrix[((teta > 0.3125) & (teta < 0.4375)) | 
                ((teta > 0.8125) & (teta < 0.9375))] = "\\"

    threshold = 5
    edge_matrix[magnitude < threshold] = " "

    return edge_matrix


def get_image_high_freq(image: Image) -> Image:
    """
    Image substracts the low frequencies by using a gaussian 
    filter to retain the high frequencies
    """
    gray_image = image.convert("L")
    blurred = gray_image.filter(ImageFilter.GaussianBlur(radius=4))
    return ImageChops.subtract(gray_image, blurred)


def save_as_colored_html(ascii_matrix, color_matrix, output_path="output.html"):
    """
    Creates an HTML file that renders the ASCII art with real colors.
    """
    # monospace is essential for alignment; line-height 1 prevents vertical gaps
    html_start = """
    <html>
    <body style="background-color: #121212; font-family: 'Courier New', monospace; font-size: 12px; line-height: 1; letter-spacing: 0;">
    <pre style="white-space: pre;">"""
    
    html_end = "</pre></body></html>"
    
    rows, cols = ascii_matrix.shape
    lines = []
    
    for y in range(rows):
        line_chars = []
        for x in range(cols):
            r, g, b = color_matrix[y, x]
            char = ascii_matrix[y, x]
            
            line_chars.append(f'<span style="color: rgb({r},{g},{b});">{char}</span>')
        
        lines.append("".join(line_chars))
    
    full_html = html_start + "\n".join(lines) + html_end
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Done! Open '{output_path}' in your web browser to see the result.")


def save_ascii_as_image(ascii_matrix: npt.NDArray, color_matrix: npt.NDArray, output_path: str="output.png"):
    # 1. Setup Font (Use a monospaced font to keep the grid aligned)
    # On Windows: "cour.ttf" (Courier), Linux: "DejaVuSansMono.ttf", Mac: "Menlo.ttc"
    try:
        font = ImageFont.truetype("Courier", 15)
    except IOError:
        font = ImageFont.load_default()

    # Get character dimensions
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    
    # 2. Calculate output image size
    rows, cols = ascii_matrix.shape
    out_width = cols * char_width
    out_height = rows * char_height
    
    # 3. Create canvas and draw
    out_image = Image.new("RGB", (out_width, out_height), color=(0, 0, 0)) # Black background
    draw = ImageDraw.Draw(out_image)

    for y in range(rows):
        for x in range(cols):
            r, g, b = color_matrix[y, x]
            char = ascii_matrix[y, x]
            # Draw character in white
            draw.text((x * char_width, y * char_height), char, font=font, fill=(r, g, b))

    out_image.save(output_path)
    print(f"Saved ASCII image to {output_path}")
