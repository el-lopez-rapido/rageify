import numpy as np
import base64
import io
import cv2
from PIL import Image

def bytes_to_opencv(inImg):
	"""takes byte sequence and returns opencv object"""
	nparr = np.fromstring(inImg, np.uint8)
	opencv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	
	return opencv_img

def bytes_to_PIL(inImg):
	"""takes byte sequence and returns PIL Image object"""
	PIL_img = Image.open(io.BytesIO(inImg))

	return PIL_img

def PIL_to_base64(inImg):
	"""takes PIL Image object and returns it encoded as base64 string"""
	buffered = io.BytesIO()
	inImg.save(buffered, format="JPEG")
	img_str = base64.b64encode(buffered.getvalue())

	return img_str

def red_filter(inImg):
	"""applies red filter on PIL Image object"""
	red_filter = (128, 0, 0, 128)
	img_overlay = Image.new(size=inImg.size, color=red_filter, mode='RGBA')
	inImg.paste(img_overlay, None, mask=img_overlay)

def find_eyes(inImg):
	"""returns coordinates of eyes found, if no face/eyes is found function returns None"""
	face_cascade = cv2.CascadeClassifier('rageifyApp/haarcascade_frontalface_default.xml')
	eye_cascade = cv2.CascadeClassifier('rageifyApp/haarcascade_eye_tree_eyeglasses.xml')

	img = bytes_to_opencv(inImg)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x, y, w, h) in faces:
		roi_gray = gray[y:y+h, x:x+w]
		eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
		coordinates = []

		for (ex, ey, ew, eh) in eyes:
			coordinates.append({"x":ex+x+int(ew/2), "y":ey+y+int(eh/2)})

		if len(coordinates) > 0:
			return coordinates

	return None

def paste_laser(inImg, coordinates):
	"""pastes laser sprite centered on passed coordinates"""
	laser = Image.open("static/laser.png")
	width, height = laser.size
	inImg.paste(laser, (coordinates["x"]-int(width/2), coordinates["y"]-int(height/2)), laser)

def process_image(inImg):
	"""performs all operations on image and returns the result encoded in base64"""
	eyes = find_eyes(inImg)
	if eyes is None:
		"""if no eyes were found, apply red filter only, and return image encoded to base64"""
		PIL_img = bytes_to_PIL(inImg)
		red_filter(PIL_img)
		base64_str = PIL_to_base64(PIL_img)
		return base64_str
	else:
		index = 0
		images = [bytes_to_PIL(inImg), bytes_to_PIL(inImg)]
		for eye in eyes:
			red_filter(images[index])
			paste_laser(images[index], eye)
			index+=1
	result = Image.blend(images[0], images[1], alpha=0.5)
	base64_str = PIL_to_base64(result)

	return base64_str