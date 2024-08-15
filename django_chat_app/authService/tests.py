from django.test import TestCase, Client
from django.contrib.auth.models import User
import json


class TestLogout(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='asdasd')

    def test_login_success(self):
        response = self.client.post('/login/', data={'username': self.user.username, 'password': 'asdasd'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(username='test_user', password='asdasd'))

    def test_login_failed(self):
        response = self.client.post('/login/', data={'username': 'username_false', 'password': 'password_false'})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)
        fields = response_json.get('fields', {})
        self.assertIn('wrong_password', fields)
        self.assertEqual(fields['wrong_password'], 'Benutzername oder Passwort falsch')
        self.assertFalse(self.client.login(username='username_false', password='password_false'))

    def test_register(self):
        response = self.client.post('/register/', data={'username': 'new_user', 'first_name': 'first_name', 'last_name': 'last_name', 'email': 'email@gmx.de', 'password': 'password', 'confirm_password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)

    def test_register_worng_password(self):
        response = self.client.post('/register/', data={'username': 'new_user', 'first_name': 'first_name', 'last_name': 'last_name', 'email': 'email@gmx.de', 'password': 'password', 'confirm_password': 'password_false'})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)

    def test_register_user_exists(self):
        response = self.client.post('/register/', data={'username': 'test_user', 'first_name': 'first_name', 'last_name': 'last_name', 'email': 'email@gmx.de', 'password': 'password', 'confirm_password': 'password'})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)

    def test_register_fields_empty(self):
        response = self.client.post('/register/', data={'username': '', 'first_name': '', 'last_name': '', 'email': '', 'password': '', 'confirm_password': ''})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)
