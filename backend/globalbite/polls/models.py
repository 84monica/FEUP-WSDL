from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=100)
    ingredients = models.TextField(default="")
    abstract = models.TextField(default="")

    def __str__(self):
        return self.name
