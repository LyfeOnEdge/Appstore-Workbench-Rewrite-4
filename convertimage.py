"""Quick script to encode image to string for use in-file"""
from PIL import Image
from io import BytesIO
def convert_tk_image_to_bytes_array(image):
	bytes_array = BytesIO()
	image.save(bytes_array, format="PNG")
	return bytes_array.getvalue()
print(convert_tk_image_to_bytes_array(Image.open("3ds.png")))