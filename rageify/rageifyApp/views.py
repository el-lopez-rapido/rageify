from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
import numpy as np
import cv2
import base64
from PIL import Image
import io
from django.contrib import messages 
from .image_processing import process_image

# Create your views here.

def ImageUploadView(request):
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			inImg = request.FILES["imageInput"].read() #uploaded image in form of byte sequence

			encodedImg = process_image(inImg)

			#encodedImg = base64.standard_b64encode(inImg) #image is encoded to base64
			decodedImg = encodedImg.decode("utf-8") #and then decoded to utf-8 in order to display it on website
			pixelate = "pixelate" in request.POST

			nparr = np.fromstring(inImg, np.uint8)
			opencv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

			##pil_img = Image.open(io.BytesIO(inImg))
			##pil_img.show()

			return render(request, "rageifyApp/index.html", {"image_data": decodedImg, "form": form})

	else:
		form = ImageForm()

	return render(request, "rageifyApp/index.html", {"form": form})
