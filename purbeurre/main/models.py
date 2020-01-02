from django.db import models

class Aliment(models.Model):
    name = models.CharField(max_length=200)
    score = models.CharField(max_length=5)
    stores = models.CharField(max_length=300)
    ingredients = models.TextField()    
    url = models.URLField()


datas = ['product_name', 'nutrition_grade_fr',
         'stores','brands','created_t','image_thumb_url',
         'code', 'ingredients',
         'nutriments', 'image_small_url', 'last_edit_dates_tags',
         'images','product_name_fr']

