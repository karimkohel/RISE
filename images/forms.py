from tkinter.tix import IMAGE
from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_file',]