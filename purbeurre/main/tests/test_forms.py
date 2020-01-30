from django.test import SimpleTestCase, TestCase
from main.forms import UserFormWithEmail
from main.form_aliment import FormAliment


class TestForms(TestCase):

    def test_expense_form_with_valid_data(self):
        form = UserFormWithEmail(data={
            'username': "antoine",
            'email':'antoine@email.com',
            'password1': 'Password5522+',
            'password2': 'Password5522+'
        })

        self.assertTrue(form.is_valid())

    def test_expense_form_with_empty_data(self):
        
        form = UserFormWithEmail(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)


class TestFormAliment(SimpleTestCase):
    
    def test_expense_form_with_valid_query(self):
        form = FormAliment(data={
            'aliments' : 'tomates',
        })
        self.assertTrue(form.is_valid())

    def test_expense_form_with_empty_data(self):
        
        form = FormAliment(data={})
        self.assertTrue(form.is_valid())
