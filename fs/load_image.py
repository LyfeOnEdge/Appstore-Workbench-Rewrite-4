from PIL import Image, ImageTk
from io import BytesIO

#Converts a png encoded in bytes to a PIL Image object
def load_image_object_from_bytes_array(bytes_array):
	return Image.open(BytesIO(bytes_array))
#Converts a png encoded in bytes to a PIL ImageTK object tkinter can process
def load_tk_image_from_bytes_array(bytes_array):
	return ImageTk.PhotoImage(load_image_object_from_bytes_array(bytes_array))