from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Aliment
import time
import requests
import json
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Dump, or update the local database from OpenFoodFact'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Lancement du programme'))

        categories = tqdm(['gateau', 'boissons', 'snacks', 'vegetarien',
                           'bonbons', 'poisson', 'alcool', 'viandes',
                           'desserts', 'pizzas', 'yaourt', 'chips',
                           'chocolat'])

        datas = ['product_name', 'nutrition_grade_fr',
                 'stores', 'brands','created_t', 'image_thumb_url',
                 'code', 'ingredients',
                 'nutriments', 'image_url', 'url',
                 'last_edit_dates_tags',
                 'images', 'product_name_fr']

        categories.set_description(' Récupération en cours: ')

        for cat in categories:
            res = []

            spec = {
                'tag_0': cat,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': 1000,
                'action': 'process',
                'json': 1
            }
# https://fr.openfoodfacts.org/cgi/search.pl?tag_0=boissons&tag_contains_0=contains&tagtype_0=categories&tag_1=fr&sort_by=unique_scans_n&page_size=1&action=process&json=1
            r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                             params=spec)
            r = r.json()
            final_list = []
            res = r['products']

            for elt in res:
                for i in datas:
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
                                   elt['code']))

                aliment = Aliment(name=elt['product_name'],
                                  name_fr=elt['product_name_fr'],
                                  date=elt['last_edit_dates_tags'],
                                  brands=elt['brands'],                               
                                  nutriscore=elt['nutrition_grade_fr'],
                                  ingredients=elt['ingredients'],
                                  image=elt['image_url'],
                                  url=elt['url'],
                                  stores=elt['stores'],
                                  code=elt['code'])
                aliment.save()

            # for i in final_list:
            #     print('')
            #     print(i[2])

        self.stdout.write(self.style.SUCCESS('Opération terminée: [OK]'))
