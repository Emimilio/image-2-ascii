
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import numpy.typing as npt


CHAR_MAP = " .icoPO?@█"
V_IDX = 2

def convert_image_to_ascii(image: Image) -> tuple[npt.NDArray, npt.NDArray]:
    width, height = image.size
    new_width, new_height = (width // 8, height // 8)

    # Resize image so every character is a pixel (character dimensions = 8x8) and convert to HSV
    image = image.resize((new_width, new_height), Image.LANCZOS)
    image_hsv = image.convert("HSV")
    ascii_matrix = np.full((new_height, new_width), " ", dtype=object)

    # Convert pixel into characters based on there luminance
    pixels_rgb = np.array(image)
    pixels_hsv = np.array(image_hsv)
    v_channel = pixels_hsv[:, :, V_IDX]

    v_func = np.vectorize(get_ascii_char_for_brightness)
    ascii_matrix = v_func(v_channel)

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


if __name__ == "__main__":

    base_dir = "./images"
    filename = "new_york"
    image_path = f"{base_dir}/{filename}.avif"
    output_path = f"{base_dir}/results/{filename}_ascii.html"
    image = Image.open(image_path)
    ascii_matrix, color_matrix = convert_image_to_ascii(image)
    save_ascii_as_image(ascii_matrix, color_matrix)
