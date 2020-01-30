from django.test import TestCase, Client
from django.urls import reverse
from main.models import Aliment, Favorite
from django.contrib.auth.models import User
import json

class TestHomePage(TestCase):

    def setUp(self):
        self.client = Client()
        self.homepage = reverse('main:homepage')


    def test_homepage_GET(self):
        ''' Testing index / homepage view method '''
        
        response = self.client.get(self.homepage)
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/1')
        self.assertEquals(response.status_code, 404)


class TestAccount(TestCase):

    def setUp(self):
        
        self.client.login(username="antoine", password="password1234")

    def test_account_is_valid(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)


class TestLogout(TestCase):

    def setUp(self):

        self.client.logout()
    
    def test_logout_view(self):
        
        response = self.client.get(reverse('main:homepage'), follow=True)
        self.assertContains(response, '<h2 class="mt-0">Colette et Remy</h2>', html=True)

class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine', 'email@email.com', 'Password3216854+')

    def test_login_success(self):

        self.client.login(username='antoine', password='Password3216854')
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)
    

class TestInfos(TestCase):

    def setUp(self):
                
        self.aliment = Aliment.objects.create(
            name ='Tomates',
            name_fr = 'Tomates cerises',
            date = '2019/01/09',
            brands = 'La Conserve',
            nutriscore = 'a',
            ingredients = 'Tomates, sel, sure, conservateurs',
            image = 'https://image-test-p8-url-test.com',
            url = 'https://test-p8-url-test.com',
            stores = 'Lidl, Auchan, Franprix',
            quantity = '200g',
            packaging = 'Conserve',
            ingredients_fr = 'Tomates, sel, sucre',
            manufactured_places = 'Dijon',
            purchase_places = 'Bordeaux, Paris',
            categories = 'Légumes',
            code = '654f654651651')
    
    def test_infos_valid_page(self):

        product = self.aliment.id        
        response = self.client.get(reverse('main:infos', args=(product,)))
        self.assertEqual(response.status_code, 200)

    # def test_infos_invalid_page(self):
        
    #     product = self.aliment.id  + 654
    #     response = self.client.get(reverse('main:infos', args=(product,)))
    #     print(response.status_code)