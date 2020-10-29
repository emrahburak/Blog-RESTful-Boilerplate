from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from corpus.models import Corpus

# Create your tests here.

class CorpusTest(APITestCase):

    url = reverse('list')

    def setUp(self):
        self.username = 'testuser'
        self.password = 'test123'
        self.owner = User.objects.create_user(username=self.username,
                                              password=self.password)

    def test_create_corpus(self):
        "create corpus"
        self.title = 'testTitle'
        self.content = 'testContent'
        self.corpus = Corpus.objects.create(owner=self.owner,
                                            title=self.title,
                                            content=self.content
                                            )
        self.assertEqual(self.corpus.title , self.title)

    def test_view_corpus_with_get(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_view_corpus_with_post(self):
        data = {
            "owner":self.owner,
            "title": "testTitle",
            "content": "testContent"
            }

        response = self.client.post(self.url, data=data)
        self.assertEqual(401, response.status_code)

        
