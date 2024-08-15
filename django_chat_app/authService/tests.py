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
