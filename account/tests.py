
import json
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User



#dogru veriler ile kayıt işlemi yap
# şifre invalid olabilir
# kullnıcı adı kullanılmış olabilir
# üye giriş yaptıysa kayıt sayfası görülmemeli
# token ile giriş işlemi yapıldığında 403 hatası


class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_token = reverse("token_obtain_pair")


    def test_user_registration(self):
        "dogru veriler ile test işlemi"

        data = {
            "username" : "testuser",
            "password" : "testpassword123"

            }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)


    def test_user_invalid_password(self):
        "yanlış (INVALID) veriler ile test işlemi"

        data = {
                "username" : "testuser",
                "password" : "2"
              }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)
    

    def test_unique_name(self):
        "Is Unique Name"

        self.test_user_registration()

        data = {
                "username" : "testuser",
                "password" : "testpassword123"
              }


        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)


    def test_user_authenticated_registration(self):

        "Session ile giriş yapmış kullanıcı Login i göremez"

        self.test_user_registration()
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)



    def test_user_authenticated_token_registration(self):

        "Token ile giriş yapmış kullanıcı Login i göremez"

        self.test_user_registration()
        data = {
                "username" : "testuser",
                "password" : "testpassword123"
              }

        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

        response_with_token = self.client.get(self.url)
        self.assertEqual(403, response_with_token.status_code)


class UserLogin(APITestCase):
    
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)


    def test_user_token(self):
        response = self.client.post(self.url_token,
                                    {"username" : "testuser",
                                     "password" : "testpassword123"})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))


    def test_user_invalid_token(self):
        response = self.client.post(self.url_token,
                                    {"username" : "invaliduser",
                                     "password" : "testpassword123"})
        self.assertEqual(401, response.status_code)
     
    def test_user_empty_data_token(self):
        response = self.client.post(self.url_token,
                                    {"username" : "",
                                     "password" : ""})
        self.assertEqual(400, response.status_code)


class UserChangePasswordTest(APITestCase):

    url = reverse('account:change-password')
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)

    def test_login_with_token(self):
        data = {
                "username" : "testuser",
                "password" : "testpassword123"
              }

        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

   


    def test_is_authenticated(self):
        "oturum açılmadan girilirse hata ver"
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


    def test_with_valid_data(self):
        self.test_login_with_token()
        data = {
            "old_password" : "testpassword123",
            "new_password" : "new_password123"
            }

        response = self.client.put(self.url, data)
        self.assertEqual(204, response.status_code)
        
    def test_with_invalid_data(self):
        self.test_login_with_token()
        data = {
            "old_password" : "invalidpassword123",
            "new_password" : "new_password123"
            }

        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)


    def test_with_empty_information(self):
        self.test_login_with_token()
        data = {
            "old_password" : "",
            "new_password" : ""
            }

        response = self.client.put(self.url, data)
        self.assertEqual(400, response.status_code)



class UserProfileUpdate(APITestCase):

    url = reverse("account:me")
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)

    def test_login_with_token(self):
        data = {
                "username" : "testuser",
                "password" : "testpassword123"
              }

        response = self.client.post(self.url_token, data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+token)

    def test_is_authenticated(self):
        "oturum açılmadan girilirse hata ver"
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)


    #def test_with_empty_information(self):
    #    self.test_login_with_token()
    #    data = {
    #        "user":{
    #        "id":1,
    #        "first_name" : "",
    #        "last_name" : ""},
    #        "profile":{
    #            "id":1,
    #            "note":"as",
    #            "twitter":"as"
    #            }
    #        }

    #    response = self.client.put(self.url, data, format='json')
    #    self.assertEqual(200, response.status_code)
    #    #self.assertEqual(json.loads(response.content), data)








        

        
    
