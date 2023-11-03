from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError

from Auth.models import User
from tascrum.models import Member
from tascrum.views import MemberProfileView, ChangePasswordView



class ProfileTest(APITestCase, SimpleTestCase):
    
    def test_profile_url(self):
        url = reverse("profile-list")
        self.assertEqual(resolve(url).func.cls, MemberProfileView)

    def test_changepassword_url(self):
        url = reverse("change-list")
        self.assertEqual(resolve(url).func.cls, ChangePasswordView)

    def test_create_user_for_Member(self):
        response = User.objects.create_user(first_name='saba', last_name='razi',email='razi.saba@gmail.com',\
                                          username= "sabarzii", password='thisissaba')
        self.assertIsInstance(response , User)
        return response
    
    def test_create_Member(self):
        response = Member.objects.create(
            user=self.test_create_user_for_Member(),
            occupations='Employee',
            bio='Another test bio',
            birthdate='1990-05-15'
        )

        self.assertIsInstance(response , Member)
        return response

    def test_Meber_fileds(self):

        user1 = User.objects.create_user(first_name='saba', last_name='razi',email='razi1.saba@gmail.com',\
                                          username= "sabarzii1", password='thisissaba')
        self.assertIsInstance(user1 , User)

        member1 = Member.objects.create(
            user= user1,
            occupations='Employee',
            bio='Another test bio',
            birthdate='1990-05-15'
        )

        self.assertIsInstance(member1 , Member)

        self.assertEqual(member1.user, user1)
        self.assertEqual(member1.occupations, 'Employee')
        self.assertEqual(member1.bio, 'Another test bio')
        self.assertEqual(str(member1.birthdate), '1990-05-15')

class changepasswordTest(APITestCase , SimpleTestCase):
    def authenticate_member(self):
        register_data = {
            'username': 'username',
            'email': 'email@gmail.com',
            'password': 'password',
        }
        response = self.client.post(reverse('user-list'), register_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        login_data = {
            'email': 'email@gmail.com',
            'password': 'password',
        }
        response = self.client.post(reverse('jwt-create-list'), login_data)
        token = response.data.get('token', None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_change_password_without_auth(self):
        response = self.client.post(reverse('change-list') , data={'password': "new_password"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_with_auth(self):
        self.authenticate_member()
        response = self.client.post(reverse('change-list') , data={'password': "new_password"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


   


