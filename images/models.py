from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Image(models.Model):

    class TypeChoices(models.TextChoices):
        DATABASE = "DATABASE", "DATABASE"
        QUERY = "QUERY", "QUERY"


    title = models.CharField(max_length=250)
    type = models.CharField(max_length=50, choices=TypeChoices.choices, default=TypeChoices.QUERY)
    image_file = models.ImageField()