from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to=None, default="")

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=100)
    ingredients = models.TextField(default="")
    abstract = models.TextField(default="")
    thumbnail = models.ImageField(upload_to=None, default="")

    def __str__(self):
        return self.name
