from django.db import models


class Aliment(models.Model):
    name = models.CharField(max_length=200)
    name_fr = models.CharField(max_length=200)
    date = models.CharField(max_length=100)
    brands = models.CharField(max_length=100)
    nutriscore = models.CharField(max_length=5)
    stores = models.CharField(max_length=300)
    ingredients = models.TextField()
    url = models.URLField()
    code = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class Farovites(models.Model):      # NOT MIGRATED YET
#     username = models.CharField(max_length=200)
#     aliment = models.ManyToManyField(Aliment)