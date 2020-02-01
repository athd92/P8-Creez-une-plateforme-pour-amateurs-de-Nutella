from django.test import TestCase, Client
from django.urls import reverse
from django.contrib import auth
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
        
        self.client = Client()
        self.client.login(username="antoine", password="password1234")

    def test_account_is_logged_in(self):
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_visitor(self):

        self.client = Client()
        response = self.client.get(reverse('main:homepage'))
        self.assertEqual(response.status_code, 200)


class TestLogout(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client.login()
        self.client.logout()

    def test_logout_redirect(self):

        response = self.client.get(reverse('main:homepage'), follow=True)
        self.assertContains(response,
                            '<h2 class="mt-0">Colette et Remy</h2>',
                            html=True)
        self.assertEqual(response.status_code, 200)


class TestLogin(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_login_success(self):

        self.client.login(username='antoine', password='Password3216854+')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, True)

    def test_login_fail(self):

        self.client.login(username='antoine', password='wrongpassword1234')
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)


class TestInfos(TestCase):

    def setUp(self):

        self.aliment = Aliment.objects.create(
            name='Tomates',
            name_fr='Tomates cerises',
            date='2019/01/09',
            brands='La Conserve',
            nutriscore='a',
            ingredients='Tomates, sel, sure, conservateurs',
            image='https://image-test-p8-url-test.com',
            url='https://test-p8-url-test.com',
            stores='Lidl, Auchan, Franprix',
            quantity='200g',
            packaging='Conserve',
            ingredients_fr='Tomates, sel, sucre',
            manufactured_places='Dijon',
            purchase_places='Bordeaux, Paris',
            categories='Légumes',
            code='654f654651651')

    def test_infos_valid_page(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:infos', args=(product,)))
        self.assertEqual(response.status_code, 200)

    def test_infos_empty_args(self):

        response = self.client.get('/infos/')
        self.assertEqual(response.status_code, 404)

    def test_infos_wrong_args(self):

        response = self.client.get('/infos/tests')
        self.assertEqual(response.status_code, 404)


class TestSaved(TestCase):

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
    

        self.aliment = Aliment.objects.create(
            name='Tomates',
            name_fr='Tomates cerises',
            date='2019/01/09',
            brands='La Conserve',
            nutriscore='a',
            ingredients='Tomates, sel, sure, conservateurs',
            image='https://image-test-p8-url-test.com',
            url='https://test-p8-url-test.com',
            stores='Lidl, Auchan, Franprix',
            quantity='200g',
            packaging='Conserve',
            ingredients_fr='Tomates, sel, sucre',
            manufactured_places='Dijon',
            purchase_places='Bordeaux, Paris',
            categories='Légumes',
            code='654f654651651')

    def test_saved_view_get_logged_in(self):

        self.client.login(username='antoine', password='Password3216854+')
        response = self.client.get(reverse('main:saved'))
        self.assertEqual(response.status_code, 200)


    def test_saved_view_get_not_logged(self):

        self.client.login(username='antoine', password='Password3216854+')
        self.client.logout()
        response = self.client.get(reverse('main:saved'))
        self.assertRedirects(response, '/login/')


class TestSaveAliment(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
        self.aliment = Aliment.objects.create(
            name='Tomates',
            name_fr='Tomates cerises',
            date='2019/01/09',
            brands='La Conserve',
            nutriscore='a',
            ingredients='Tomates, sel, sure, conservateurs',
            image='https://image-test-p8-url-test.com',
            url='https://test-p8-url-test.com',
            stores='Lidl, Auchan, Franprix',
            quantity='200g',
            packaging='Conserve',
            ingredients_fr='Tomates, sel, sucre',
            manufactured_places='Dijon',
            purchase_places='Bordeaux, Paris',
            categories='Légumes',
            code='654f654651651')

    def test_save_aliment_view(self):

        product = self.aliment.id
        self.client.login(username='antoine', password='Password3216854+')
        aliment_saved = Favorite.objects.create(saved_by=self.user,
                                                saved_aliment=self.aliment)
        aliments_saved = Favorite.objects.filter(saved_by=self.user,
                                                 saved_aliment=self.aliment)
        self.assertTrue(aliments_saved.exists())


class TestAlternative(TestCase):

    def setUp(self):

        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')
        self.client = Client()
        self.aliment = Aliment.objects.create(
            name='Tomates',
            name_fr='Tomates cerises',
            date='2019/01/09',
            brands='La Conserve',
            nutriscore='a',
            ingredients='Tomates, sel, sure, conservateurs',
            image='https://image-test-p8-url-test.com',
            url='https://test-p8-url-test.com',
            stores='Lidl, Auchan, Franprix',
            quantity='200g',
            packaging='Conserve',
            ingredients_fr='Tomates, sel, sucre',
            manufactured_places='Dijon',
            purchase_places='Bordeaux, Paris',
            categories='Légumes',
            code='654f654651651')

    def test_get_alternative(self):

        product = self.aliment.id
        response = self.client.get(reverse('main:alternative',
                                   args=(product, )))
        self.assertEqual(response.status_code, 200)

    def test_get_alternative_with_adds(self):

        product = self.aliment.id + 1
        response = self.client.get(reverse('main:alternative',
                                           args=(product, )))
        self.assertEqual(response.status_code, 302)
        

class TestDelete(TestCase):

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_delete_logged_user(self):

        self.client.login(username='antoine', password='Password3216854+')
        response = self.client.get(reverse('main:delete', args=("1")))
        self.assertEqual(response.status_code, 302)
    
    def test_delete_not_logged_user(self):

        self.client.login(username='antoine', password='Password3216854+')
        self.client.logout()
        response = self.client.get(reverse('main:delete', args=('1')))
        self.assertEqual(response.status_code, 302)


class TestRegister(TestCase):

    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user('antoine',
                                             'email@email.com',
                                             'Password3216854+')

    def test_get_register_page(self):

        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)

    # def test_registration_invalid_infos(self):

    #     response = self.client.post(reverse('main:register'),
    #                                 data={'username': 'antoine',
    #                                       'email': 'antoine@email.com',
    #                                       'password1': 'pasword121331+',
    #                                       'password2': 'pasword121331+'})

    #     self.assertRedirects(response, reerse('/homepage/'))
