from django.core.management.base import BaseCommand, CommandError
import requests
import json
from tqdm import tqdm

# from main.models import Aliment

class Command(BaseCommand):
    help = 'Dump or update the local database from OpenFoodFact'

    def handle(self, *args, **kwargs):
        self.stdout.write('Lancement du programme')

        categories = ['gateau', 'boissons', 'snacks', 'vegetarien', 'bonbons', 'poisson',
                    'alcool', 'viandes', 'desserts', 'pizzas']

        datas = ['product_name', 'nutrition_grade_fr',
                'stores','brands','created_t','image_thumb_url',
                'code', 'ingredients',
                'nutriments', 'image_small_url', 'last_edit_dates_tags',
                'images','product_name_fr']



        for cat in tqdm(categories):

            res = []


            payload = {
                'tag_0': cat,
                'tag_contains_0': 'contains',
                'tagtype_0': 'categories',
                'tag_1': 'fr',
                'tag_contains_1': 'contains',
                'tagtype_1': 'lang',
                'sort_by': 'unique_scans_n',
                'page_size': 1,
                'action': 'process',
                'json': 1
            }

            response = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                    params=payload)


            response = response.json()



            final_list = []

            res = response['products']

            for elt in res:
                for i in datas:
                    if not elt.get(i):
                        elt[i] = "non disponible"
                
                final_list.append((elt['product_name'], elt['last_edit_dates_tags'],
                                        elt['brands'], elt['nutrition_grade_fr'],
                                        elt['url'],elt['stores']))



            for i in final_list:
                print('')
                print(i)
            
        self.stdout.write(self.style.SUCCESS('Opération terminée: [OK]'))


