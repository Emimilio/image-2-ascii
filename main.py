
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import numpy.typing as npt


CHAR_MAP = " .icoPO?@█"

def convert_image_to_ascii(image: Image) -> tuple[npt.NDArray, npt.NDArray]:
    image = image.convert("RGB")
    width, height = image.size
    new_width, new_height = (width // 8, height // 8)

    # Resize image so every character is a pixel (character dimensions = 8x8) and convert to HSV
    image = image.resize((new_width, new_height), Image.LANCZOS)
    image_hsv = image.convert("HSV")
    ascii_matrix = np.full((new_height, new_width), " ", dtype=object)

    # Convert pixel into characters based on there luminance
    pixels_rgb = image.load()
    pixels_hsv = image_hsv.load()
    for x in range(new_width):
        for y in range(new_height):
            h, s, v = pixels_hsv[x, y]
            ascii_matrix[y, x] = get_ascii_char_for_brightness(v)

    return ascii_matrix, pixels_rgb


def get_ascii_char_for_brightness(v: float) -> str:
    idx = int(v / 255 * (len(CHAR_MAP) - 1))
    return CHAR_MAP[idx]


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
            r, g, b = color_matrix[x, y]
            char = ascii_matrix[y, x]
            
            line_chars.append(f'<span style="color: rgb({r},{g},{b});">{char}</span>')
        
        lines.append("".join(line_chars))
    
    full_html = html_start + "\n".join(lines) + html_end
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Done! Open '{output_path}' in your web browser to see the result.")


if __name__ == "__main__":

    base_dir = "./images"
    filename = "banana"
    image_path = f"{base_dir}/{filename}.webp"
    output_path = f"{base_dir}/{filename}_ascii.html"
    image = Image.open(image_path)
    ascii_matrix, color_matrix = convert_image_to_ascii(image)
    save_as_colored_html(ascii_matrix, color_matrix, output_path)
