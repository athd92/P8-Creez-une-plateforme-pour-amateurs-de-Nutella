
from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Aliment
import time
import requests
import json
from tqdm import tqdm
import requests
import datetime


class Command(BaseCommand):
    help = 'Update the database every 7 days from de OpenFoodFact API REST'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(
            'Lancement de la mise à jour de la base de données'))

        r = 7
        dates_list = []
        current_date = datetime.datetime.today()  # get current day
        for i in range(r):  # get 7 previous days
            d = current_date - datetime.timedelta(days=r)
            dates_list.append(str(d.date()))
            r = r - 1

        categories = ['gateau', 'boissons', 'snacks', 'vegetarien',
                      'bonbons', 'poisson', 'alcool', 'viandes',
                      'desserts', 'pizzas', 'yaourt', 'chips',
                      'chocolat']

        datas = ['product_name', 'product_name_fr', 'last_edit_dates_tags',
                 'brands', 'nutrition_grade_fr', 'ingredients', 'image_url',
                 'url', 'stores', 'quantity', 'packaging',
                 'ingredients_text_fr', 'manufacturing_places',
                 'purchase_places', 'categories', 'code']

        for i in tqdm(dates_list):
            for cat in tqdm(categories):
                res = []
                spec = {
                    'last_edit_dates_tags': dates_list,
                    'tag_0': cat,
                    'tag_contains_0': 'contains',
                    'tagtype_0': 'categories',
                    'tag_1': 'fr',
                    'tag_contains_1': 'contains',
                    'tagtype_1': 'lang',
                    'sort_by': 'unique_scans_n',
                    'page_size': 20,
                    'action': 'process',
                    'json': 1
                }
                r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                 params=spec)
                r = r.json()
                final_list = []
                res = r['products']

            for elt in tqdm(res):
                for i in tqdm(datas):
                    if not elt.get(i):
                        elt[i] = "non disponible"

                final_list.append((elt['product_name'],
                                   elt['product_name_fr'],
                                   elt['last_edit_dates_tags'][0],
                                   elt['brands'],
                                   elt['nutrition_grade_fr'],
                                   elt['ingredients'],
                                   elt['image_url'],
                                   elt['url'],
                                   elt['stores'],
                                   elt['quantity'],
                                   elt['packaging'],
                                   elt['ingredients_text_fr'],
                                   elt['manufacturing_places'],
                                   elt['purchase_places'],
                                   elt['categories'],
                                   elt['code']))

                aliment = Aliment(
                    name=elt['product_name'],
                    name_fr=elt['product_name_fr'],
                    date=elt['last_edit_dates_tags'],
                    brands=elt['brands'],
                    nutriscore=elt['nutrition_grade_fr'],
                    ingredients=elt['ingredients'],
                    image=elt['image_url'],
                    url=elt['url'],
                    stores=elt['stores'],
                    quantity=elt['quantity'],
                    packaging=elt['packaging'],
                    ingredients_fr=elt['ingredients_text_fr'],
                    manufactured_places=elt['manufacturing_places'],
                    purchase_places=elt['purchase_places'],
                    categories=elt['categories'],
                    code=elt['code'])
                aliment.save()
                total_count = Aliment.objects.count()

        self.stdout.write(self.style.SUCCESS('Opération terminée: [OK]'))
        self.stdout.write(self.style.SUCCESS(
            f'Nombre d\'aliments ajoutés: {total_count}'))
        self.stdout.write(self.style.SUCCESS(
            'La base de données a été mise à jour avec succès!'))
