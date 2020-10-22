
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from post.models import Post


class UserLogin(APITestCase):
    
    url_login = reverse("token_obtain_pair")
    url_create = reverse("post:create")
    url_list = reverse("post:list")

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)

        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        "jwt_authentication"
        response = self.client.post(self.url_login,
                                    {"username" : self.username,
                                     "password" : self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)


    def test_add_new_post(self):
        "add new post"
        data = {
            'title':'başlik',
            'content':'icerik'
            }

        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)


    def test_add_new_post_unauthorization(self):
        "add new post without authentication"
        self.client.credentials()

        data = {
            'title':'baslik',
            'content': 'icerik',
            }

        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)
        


    def test_post_list(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)['results']) == Post.objects.all().count())

            

class PostUpdateDelete(APITestCase):

    url_login = reverse("token_obtain_pair")
    url_create = reverse("post:create")
    url_list = reverse("post:list")

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.user2 = User.objects.create_user(username='testuser2',
                                              password='testpassword1234')

        self.post = Post.objects.create(user=self.user,title='başlık', content='içerik')
        self.url = reverse('post:update',kwargs={'slug':self.post.slug})

        self.test_jwt_authentication()

    def test_jwt_authentication(self, username='testuser', password='testpassword123'):
        "jwt_authentication"
        response = self.client.post(self.url_login,
                                    {"username" : username,
                                     "password" : password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)


    def test_post_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_post_delete_different_user(self):
        self.test_jwt_authentication('testuser2','testpassword1234')
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    def test_post_update(self):
        data = {

            'title':'baslik',
            'content':'icerik'
            }

        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Post.objects.get(id=self.post.id).content == data['content'])
