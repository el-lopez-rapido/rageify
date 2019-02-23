from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageForm
import numpy as np
import cv2
import base64
from django.contrib import messages 

# Create your views here.

def ImageUploadView(request):
	if request.method == "POST":
		form = ImageForm(request.POST, request.FILES)
		if form.is_valid():
			inImg = request.FILES["imageInput"].read() #uploaded image in form of byte sequence
			encodedImg = base64.standard_b64encode(inImg) #image is encoded to base64
			decodedImg = encodedImg.decode("utf-8") #and then decoded to utf-8 in order to display it on website

			return render(request, "rageifyApp/base.html", {"image_data": decodedImg, "form": form})

	else:
		form = ImageForm()

	return render(request, "rageifyApp/base.html", {"form": form})
