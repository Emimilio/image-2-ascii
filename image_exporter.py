
from PIL import ImageDraw, ImageFont, Image
import numpy.typing as npt

def save_as_colored_html(ascii_matrix, color_matrix, output_path="output.html"):
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

    print(f"Saved HTML image to {output_path}")


def save_ascii_as_image(ascii_matrix: npt.NDArray, color_matrix: npt.NDArray, output_path: str="output.png"):
    out_image = draw_image(ascii_matrix, color_matrix)
    out_image.save(output_path)
    print(f"Saved ASCII image to {output_path}")


def draw_image(ascii_matrix: npt.NDArray, color_matrix: npt.NDArray) -> Image:
    try:
        font = ImageFont.truetype("Courier", 15)
    except IOError:
        font = ImageFont.load_default()

    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    
    rows, cols = ascii_matrix.shape
    out_width = cols * char_width
    out_height = rows * char_height
    
    out_image = Image.new("RGB", (out_width, out_height), color=(0, 0, 0))
    draw = ImageDraw.Draw(out_image)

    for y in range(rows):
        for x in range(cols):
            r, g, b = color_matrix[y, x]
            char = ascii_matrix[y, x]
            draw.text((x * char_width, y * char_height), char, font=font, fill=(r, g, b))

    return out_image

def draw_image_to_terminal(ascii_matrix: npt.NDArray, color_matrix: npt.NDArray):
    lines = []
    for char_row, color_row in zip(ascii_matrix, color_matrix):

        line_chars = []
        for char, color in zip(char_row, color_row):
            r, g, b = color
            ansi_char = f"\033[38;2;{int(r)};{int(g)};{int(b)}m{char}"
            line_chars.append(ansi_char)

        lines.append("".join(line_chars) + "\033[0m")

    full_output = "\n".join(lines)
    print(full_output)
