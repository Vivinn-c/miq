from PIL import Image, ImageDraw, ImageFont
def getsize(font, text):
    left, top, right, bottom = font.getbbox(text)
    return right - left, bottom 

# Set up the main image
main_image = Image.new("RGB", (300, 400), "white")
draw = ImageDraw.Draw(main_image)

# Load a regular font
font_path = "fonts/MPLUSRounded1c-Regular.ttf"  # Replace with the path to your font
font = ImageFont.truetype(font_path, 40)

# Calculate the size of the text box
text = "Hello World"
text_width, text_height = getsize(font, text)

# Create a transparent image for the text with exact text box size
text_image = Image.new("RGBA", (text_width + 10, text_height + 10), (255, 255, 255, 0))
text_draw = ImageDraw.Draw(text_image)

# Draw the text on the transparent image
text_draw.text((0, 0), text, font=font, fill="black")

# Apply an affine transformation to skew only the text
text_image = text_image.transform(
    (text_image.width, text_image.height),
    Image.AFFINE,
    (1, -0.3, 0, 0, 1, 0),  # Adjust skew by modifying the -0.3 value
    Image.BICUBIC
)

# Paste the skewed text image onto the main image at desired position
main_image.paste(text_image, (10, 20), text_image)  # Use text_image as mask to maintain transparency

# Show and save the image
main_image.show()
main_image.save("output.png")

