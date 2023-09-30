from PIL import Image, ImageDraw, ImageFont
import sys

def image_to_reversed_ascii(image_path, output_width=None):
    """
    Convert the provided image to a reversed (darker) high-resolution ASCII representation.
    """
    # Reversed set of ASCII characters ordered by their visual density
    ascii_chars = list("#@8%*+=-:. ")
    
    # Load the image
    img = Image.open(image_path)
    
    # Calculate aspect ratio and desired width
    aspect_ratio = img.height / img.width
    if output_width:
        output_height = int(aspect_ratio * output_width)
    else:
        output_width = img.width
        output_height = img.height

    # Resize the image
    img = img.resize((output_width, output_height))
    
    # Convert the image to grayscale
    img = img.convert("L")
    
    # Convert each pixel to the appropriate ASCII character
    pixels = list(img.getdata())
    ascii_image = [ascii_chars[pixel * len(ascii_chars) // 256] for pixel in pixels]
    
    # Split the ASCII image into lines
    ascii_image = [ascii_image[index: index + output_width] for index in range(0, len(ascii_image), output_width)]
    
    # Convert the ASCII image into a string format
    return "\n".join(["".join(row) for row in ascii_image])

def ascii_art_to_image_small_font(ascii_art, font_size=6):
    """
    Convert ASCII art to an image using a smaller font.
    """
    # Use the default PIL font
    font = ImageFont.load_default()

    # Calculate the size required for the image
    ascii_lines = ascii_art.split("\n")
    max_width = max([font.getsize(line)[0] for line in ascii_lines])
    total_height = len(ascii_lines) * font_size

    # Create a new white image with the calculated size
    image = Image.new("L", (max_width, total_height), 255)
    draw = ImageDraw.Draw(image)

    # Draw each line of the ASCII art on the image
    y_position = 0
    for line in ascii_lines:
        draw.text((0, y_position), line, font=font, fill=0)
        y_position += font_size

    return image

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <path_to_image>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    reversed_ascii_art = image_to_reversed_ascii(image_path, output_width=300)
    ascii_image_result = ascii_art_to_image_small_font(reversed_ascii_art)
    
    output_image_path_result = image_path.rsplit('.', 1)[0] + "_reversed_ascii.png"
    ascii_image_result.save(output_image_path_result)
    print(f"Saved ASCII art image to: {output_image_path_result}")
