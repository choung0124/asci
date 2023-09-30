from PIL import Image, ImageDraw, ImageFont
import numpy as np

def image_to_aspect_maintained_ascii_expanded(image_path, output_width=None, char_aspect_ratio=2.2):
    """Convert the provided image to a high-resolution ASCII representation while expanding horizontally."""
    ascii_chars = list("#@8%*+=-:. ")
    img = Image.open(image_path)
    original_aspect_ratio = img.height / img.width

    if output_width:
        adjusted_output_width = int(output_width * char_aspect_ratio)
        output_height = int(adjusted_output_width * original_aspect_ratio / char_aspect_ratio)
    else:
        adjusted_output_width = int(img.width * char_aspect_ratio)
        output_height = img.height

    img = img.resize((adjusted_output_width, output_height), Image.ANTIALIAS)
    img = img.convert("L")
    pixels = list(img.getdata())
    ascii_image = [ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels]
    ascii_image = [ascii_image[index: index + adjusted_output_width] for index in range(0, len(ascii_image), adjusted_output_width)]
    return "\n".join(["".join(row) for row in ascii_image])

def ascii_art_to_image_square_aspect(ascii_art, font_size=10, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
    """Convert ASCII art to an image using a monospaced font with a square aspect ratio."""
    font = ImageFont.truetype(font_path, font_size)
    ascii_lines = ascii_art.split("\n")
    max_width = max([len(line) for line in ascii_lines]) * font_size
    total_height = len(ascii_lines) * font_size

    image = Image.new("L", (max_width, total_height), 255)
    draw = ImageDraw.Draw(image)
    y_position = 0
    for line in ascii_lines:
        draw.text((0, y_position), line, font=font, fill=0)
        y_position += font_size
    return image

def trim_whitespace(image):
    """Trim whitespace from the right side of an image."""
    img_array = np.array(image)
    col_sum = np.sum(img_array, axis=0)
    last_col_index = np.where(col_sum < 255 * img_array.shape[0])[0][-1]
    img_array_cropped = img_array[:, :last_col_index+1]
    return Image.fromarray(img_array_cropped)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the image as an argument.")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_width = 600

    # Convert to ASCII
    ascii_art = image_to_aspect_maintained_ascii_expanded(image_path, output_width)
    # Render ASCII to image
    ascii_image = ascii_art_to_image_square_aspect(ascii_art)
    # Trim whitespace
    trimmed_image = trim_whitespace(ascii_image)

    # Save results
    ascii_image.save("ascii_output.png")
    trimmed_image.save("trimmed_output.png")
    with open("ascii_output.txt", 'w') as file:
        file.write(ascii_art)
