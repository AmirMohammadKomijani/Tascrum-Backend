from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from Auth.models import User
from django.db import IntegrityError

##tests are here

class AuthTest(APITestCase, SimpleTestCase):

    def setUp(self):
        self.user = User.objects.create_user(first_name='saba', last_name='razi',email='razi.saba@gmail.com',\
                                          username= "sabarzii", password='thisissaba')
        self.assertIsInstance(self.user, User)
    
    # def test_login_url(self):
    #     url = reverse("auth/users")
    #     print(resolve(url))

    def test_user_email(self):
        self.assertEqual(self.user.email, 'razi.saba@gmail.com')
    
    def test_user_username(self):
        self.assertEqual(self.user.username, 'sabarzii')
    
    def test_user_error_when_no_username(self):
        self.assertRaises(ValueError, User.objects.create_user, username="",
                          email='hi@gmail.com', password='password123!@')
    
    # def test_user_error_when_no_password(self):
    #     self.assertRaises(ValueError, User.objects.create_user, username="thisishi",
    #                       email='thisshi@gmail.com', password='')
    
    # def test_user_error_when_no_email(self):
    #     self.assertRaises(ValueError, User.objects.create_user, username="thisishi2",
    #                       email='', password='eybaba')

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="anotheruser",
                email="razi.saba@gmail.com",
                password="anotherpassword"
            )

    def test_user_groups(self):
        group = self.user.groups.create(name="Test Group")
        self.assertIn(group, self.user.groups.all())

    def test_number_of_users(self):
        user = User.objects.create_user(first_name='amir', last_name='komij',email='komij@gmail.com',\
                                          username= "komijaniii", password='thisiskomij')
        self.assertEqual(User.objects.all().count(), 2)
    
    # def delete_one_user(self):
    #     response = self.client.delete(
    #         reverse("create", kwargs={'username': "sabarzii"}))
        
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Todo.objects.all().count(), 0)