from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APIClient
from datetime import datetime
from django.test import TestCase
from Auth.models import User
from tascrum.models import *
from tascrum.views import *



class TestModels(TestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(
            name='Workspace test',
            type='small business',
            description='Workspace description',
        )
        self.board = Board.objects.create(title='Board test', workspace=self.workspace)
        self.list1 = List.objects.create(title='List test', board=self.board)
        self.card1 = Card.objects.create(
            title='card',
            list=self.list1,
            startdate=timezone.now(),
            duedate=timezone.now() + timezone.timedelta(days=7),
            description='Default card description',
            storypoint=0,
            setestimate=0,
            reminder='1 Day before',
            order=1,  # Provide the appropriate order value
            status='pending'
        )

        user1 = User.objects.create_user(first_name='amir', last_name='komij',email='komij1.amir@gmail.com',\
                                          username= "test username", password='thisisamir')
        self.member = Member.objects.create(
            user= user1,
            occupations='Employee',
            bio='Another test bio',
            birthdate='1990-05-15'
        )    
    def test_card_title(self):
        self.assertEqual(self.card1.title, 'card')
    def test_card_storypoint(self):
        self.assertEqual(self.card1.storypoint, 0)
    def test_card_setestimate(self):
        self.assertEqual(self.card1.setestimate, 0)
    # def test_card_duedate(self):
    #     self.assertEqual(self.card1.duedate, timezone.now() + timezone.timedelta(days=7))
    def test_card_reminder(self):
        self.assertEqual(self.card1.reminder, '1 Day before')

    def test_member_bio(self):
        self.assertEqual(self.member.bio, 'Another test bio')
    def test_member_birthdate(self):
        self.assertEqual(self.member.birthdate, '1990-05-15')
    def test_member_occupations(self):
        self.assertEqual(self.member.occupations, 'Employee')
    def test_member_firstName(self):
        self.assertEqual(self.member.user.first_name, 'amir')
    def test_member_lastName(self):
        self.assertEqual(self.member.user.last_name, 'komij')
    def test_member_userName(self):
        self.assertEqual(self.member.user.username, 'test username')
    def test_member_email(self):
        self.assertEqual(self.member.user.email, 'komij1.amir@gmail.com')


class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.assign_url = reverse('assign-list')

        self.workspace = Workspace.objects.create(
            name='Workspace test',
            type='small business',
            description='Workspace description',
        )
        self.board = Board.objects.create(title='Board test', workspace=self.workspace)
        self.list1 = List.objects.create(title='List test', board=self.board)
        self.card1 = Card.objects.create(
            title='card',
            list=self.list1,
            startdate=timezone.now(),
            duedate=timezone.now() + timezone.timedelta(days=7),
            description='Default card description',
            storypoint=0,
            setestimate=0,
            reminder='1 Day before',
            order=1,  # Provide the appropriate order value
            status='pending'
        )

        user1 = User.objects.create_user(first_name='amir', last_name='komij',email='komij1.amir@gmail.com',\
                                          username= "test username", password='thisisamir')
        self.member = Member.objects.create(
            user= user1,
            occupations='Employee',
            bio='Another test bio',
            birthdate='1990-05-15'
        )    

    def authenticate(self):
        register_data = {
            'first_name':'test fname',
            'last_name':'test lname',
            'username': 'test username',
            'email': 'fortest@gmail.com',
            'password': 'Somepass',
        }
        response = self.client.post(reverse('user-list'), register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # User login
        login_data = {
            'email': 'fortest@gmail.com',
            'password': 'Somepass',
        }
        response = self.client.post(reverse('jwt-create'), login_data)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["access"] is not None)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_Assign(self):
        self.authenticate()
        create_assign_data = {
            'card': self.card1.id,
            'member': self.member.id 
        }

        # Send a POST request to create a new list
        response = self.client.post(self.assign_url, create_assign_data, format='json')

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Optionally, you can check the response data for additional details
        self.assertEqual(response.data['card'], self.card1.id)
        self.assertEqual(response.data['member'], self.member.id)

        # Optionally, you can check if the new list is actually created in the database
        new_assign = MemberCardRole.objects.get(card=self.card1.id, member=self.member)
        self.assertIsNotNone(new_assign)


class TestUrls(APITestCase):

    def test_List_is_resolved(self):
        url = reverse('assign-list')
        self.assertEquals(resolve(url).func.cls, CardAssignmentView)