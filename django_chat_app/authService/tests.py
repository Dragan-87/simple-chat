from django.test import TestCase, Client
from django.contrib.auth.models import User
import json


class TestLogout(TestCase):
    def test_login_success(self):
        self.user = User.objects.create_user(username='test_user', password='asdasd')
        response = self.client.post('/login/', data={'username': self.user.username, 'password': self.user.password})
        assert response.status_code == 200
        assert self.user.is_authenticated

    def test_login_failed(self):
        self.user = User.objects.create_user(username='test_user', password='asdasd')
        response = self.client.post('/login/', data={'username': 'username_flase', 'password': 'password_false'})
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content.decode())
        self.assertIn('fields', response_json)
        fields = response_json.get('fields', {})
        self.assertIn('wrong_password', fields)
        self.assertEqual(fields['wrong_password'], 'Benutzername oder Passwort falsch')
