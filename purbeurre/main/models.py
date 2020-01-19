from django.db import models


class Aliment(models.Model):
    name = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    date = models.TextField(max_length=100)
    brands = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=100)
    ingredients = models.TextField()
    image = models.URLField(max_length=255)
    url = models.URLField(max_length=255)
    stores = models.CharField(max_length=300)
    quantity = models.CharField(max_length=300)
    packaging = models.CharField(max_length=600)
    ingredients_fr = models.TextField()
    manufactured_places = models.CharField(max_length=1000)
    purchase_places = models.CharField(max_length=500)
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.name









# class Farovites(models.Model):      # NOT MIGRATED YET
#     username = models.CharField(max_length=200)
#     aliment = models.ManyToManyField(Aliment)