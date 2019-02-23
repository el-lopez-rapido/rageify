from django import forms

class ImageForm(forms.Form):
    imageInput = forms.ImageField(label = "Image")
    pixelate = forms.BooleanField(initial=True, required=False)