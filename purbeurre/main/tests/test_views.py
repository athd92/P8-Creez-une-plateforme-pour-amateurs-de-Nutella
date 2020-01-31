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
        self.assertContains(response,
                            '<h2 class="mt-0">Colette et Remy</h2>',
                            html=True)


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

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

    def test_invalid_url(self):

        response = self.client.get('/infos/')
        self.assertEqual(response.status_code, 404)



class TestSaved(TestCase):

    def setUp(self):

        self.client = Client()
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

    def test_saved_view(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:saved'))
        self.assertEqual(response.status_code, 200)

    def test_saved_empty(self):

        response = self.client.get(reverse("main:saved"))
        self.assertEqual(response.status_code, 200)


class TestSaveAliment(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
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

    def test_save_aliment_view(self):

        product = self.aliment.id
        self.client.login(username='antoine', password='Password3216854+')
        aliment_saved = Favorite.objects.create(saved_by=self.user, saved_aliment=self.aliment)
        aliments_saved = Favorite.objects.filter(saved_by=self.user, saved_aliment=self.aliment)
        self.assertTrue(aliments_saved.exists())


class TestAlternative(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
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

    def test_get_alternative(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:alternative', args=(product, )))
        self.assertEqual(response.status_code, 200)


class TestDelete(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
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

    def test_delete(self):

        user = self.user
        aliment = self.aliment
        favorite_aliment = Favorite.objects.filter(
            saved_aliment=aliment,
            saved_by=user.id
        )
        favorite_aliment.delete()
        response = self.client.get(reverse('main:saved'))
        self.assertEqual(response.status_code, 200)


class TestRegister(TestCase):

    def setUp(self):

        self.client = Client()


    def test_register_view_get(self):

        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)

    def test_registration_post_success(self):

        response = self.client.post(reverse('main:register'),
                                    data={'username': 'antoine',
                                          'email': 'antoine@email.com',
                                          'password1': 'password121331+',
                                          'password2': 'password121331+'})
        self.assertRedirects(response, '/')


    # def test_registration_invalid_infos(self):

    #     response = self.client.post(reverse('main:register'),
    #                                 data={'username': 'antoine',
    #                                       'email': 'antoine@email.com',
    #                                       'password1': 'pasword121331+',
    #                                       'password2': 'password121331+'})
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(response, reverse('main:register'))

