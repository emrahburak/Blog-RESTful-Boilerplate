
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from corpus.models import Corpus
from rest_framework.routers import DefaultRouter
from corpus import views
import json

# Create a router and register our viewsets with it

router = DefaultRouter()

router.register(r'corpus', views.CorpusViewSet)
router.register(r'users', views.UserViewSet)


# Create your tests here.

class CorpusTest(APITestCase):

    url = reverse('corpus-list')
    url_login = reverse("token_obtain_pair")
    url_users = reverse('user-list')

    def setUp(self):
        self.username = 'testuser'
        self.password = 'test123'
        self.owner = User.objects.create_user(
            username=self.username, password=self.password)
        self.owner2 = User.objects.create_user(
            username='testuser2', password=self.password)

        self.corpus = Corpus.objects.create(
            owner=self.owner, title='testtitle', content='testcontent')
        self.url_detail = reverse(
            'corpus-detail', kwargs={'slug': self.corpus.slug})

        self.test_jwt_authentication()


    def test_get_users(self):
        "readonly user_list"
        response = self.client.get(self.url_users)

        self.assertEqual(200, response.status_code)
        

    def test_jwt_authentication(self, username='testuser', password='test123'):
        " jwt authentication "
        response = self.client.post(self.url_login, data={'username': username, 'password': password}
                                    )
        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in json.loads(response.content))
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_to_corpus(self):
        " add to corpus "
        data = {
            'title': 'test-title',
            'content': 'test-content'
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_add_to_corpus_unautharization(self):
        " add to corpus with unautharization"
        self.client.credentials()
        data = {
            'title': 'test-title',
            'content': 'test-content'
        }

        response = self.client.post(self.url, data)
        self.assertEqual(401, response.status_code)

    def test_get_corpus(self):
        "test get corpus"
        self.test_add_to_corpus()
        response = self.client.get(self.url)

        self.assertTrue(len(json.loads(response.content)["results"])
                        == Corpus.objects.all().count())

    def test_update_corpus(self):
        "corpus detail  update with auht user"

        data = {
            'title': 'updated-test-title',
            'content': 'updated-test-content'
        }

        response = self.client.put(self.url_detail, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Corpus.objects.get(id=self.corpus.id)
                        .content == data['content']
                        and Corpus.objects.get(id=self.corpus.id)
                        .title == data['title'])

    def test_update_corus_diffrent_user(self):
        "corpus-detail update with unauth- entry"
        self.test_jwt_authentication('testuser2')
        data = {
            'title': 'updated-test-title',
            'content': 'updated-test-content'
        }

        response = self.client.put(self.url_detail, data)
        self.assertEqual(403, response.status_code)
        self.assertFalse(Corpus.objects.get(id=self.corpus.id).title
                         == data['title'])

    def test_corpus_delete(self):
        "corpus detail delete with auth user "
        response = self.client.delete(self.url_detail)
        self.assertEqual(204, response.status_code)

    def test_copus_delete_diffrent_user(self):
        "corpus detail delete with diffrent auth-user"
        self.test_jwt_authentication('testuser2')
        response = self.client.delete(self.url_detail)
        self.assertEqual(403, response.status_code)

    def test_corpus_detail_unauthorization(self):
        "unautharization corpus detail read only"
        self.client.credentials()
        response = self.client.get(self.url_detail)
        self.assertEqual(200, response.status_code)


    def test_corpus_search_filter(self):
        "search filter is correct for corpus"
        url_search_filter = self.url + '?search=t'
        response = self.client.get(url_search_filter)

        self.assertEqual(200, response.status_code)


    def test_corpus_custom_owner__username_filter(self):
        "custom  owner__username filter is correct for corpus"

        url_username_filter = self.url + '?username=testuser'
        response = self.client.get(url_username_filter)

        self.assertEqual(200, response.status_code)


    def test_users_search_filter(self):
        "search filter is correct for users"
        url_search_filter = self.url_users + '?search=t'
        response = self.client.get(url_search_filter)

        self.assertEqual(200, response.status_code)


    def test_usres_username_filter(self):
        "custom  owner__username filter is correct for corpus"

        url_username_filter = self.url_users + '?username=testuser'
        response = self.client.get(url_username_filter)

        self.assertEqual(200, response.status_code)






        


        
