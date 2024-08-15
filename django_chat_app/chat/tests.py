import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Message, Chat

class ChatViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.chat = Chat.objects.create(id=1)
        self.message = Message.objects.create(text='Test message', chat=self.chat, author=self.user, receiver=self.user)

    def test_index(self):
        response = self.client.post('/chat/', {'textmessage': self.message.text})
        self.assertLessEqual(response.status_code, 399)

        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content)
        self.assertIn('fields', data)
        data = json.loads(response.content)
        self.assertIn('fields', data)
