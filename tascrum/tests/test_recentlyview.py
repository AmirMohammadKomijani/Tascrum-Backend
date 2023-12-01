from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APIClient
from datetime import datetime

from Auth.models import User
from tascrum.models import *
from tascrum.views import *

class BoardViewTest(APITestCase, SimpleTestCase):
    def setUp(self):
        self.client = APIClient()
        user1 = User.objects.create_user(first_name='saba', last_name='razi',email='razi1.saba@gmail.com',\
                                          username= "test username", password='thisissaba')
        self.members = Member.objects.create(
            user= user1,
            occupations='Employee',
            bio='Another test bio',
            birthdate='1990-05-15'
        )

        self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')

        self.board1 = Board.objects.create(
            title='board test1',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board1.members.add(self.members)

        self.board2 = Board.objects.create(
            title='board test2',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board2.members.add(self.members)

        self.board3 = Board.objects.create(
            title='board test3',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board3.members.add(self.members)

        self.board4 = Board.objects.create(
            title='board test4',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board4.members.add(self.members)
    
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

        login_data = {
            'email': 'fortest@gmail.com',
            'password': 'Somepass',
        }
        response = self.client.post(reverse('jwt-create'), login_data)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["access"] is not None)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_recentlyview_url_viewclass(self):
        url = reverse("recentlyviewed-list")
        self.assertEqual(resolve(url).func.cls, BoardRecentlyViewedView)

    def test_recentlyview_url(self):
        self.authenticate()
        url = reverse("recentlyviewed-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_count(self):
        self.assertEqual(Board.objects.all().count(), 4)

    def test_output_instancetype(self):
        self.authenticate()
        url = reverse("recentlyviewed-list")
        response = self.client.get(url)
        
        for item in response.data:
            self.assertIsInstance(item, Board)
    
    def test_board_lastseen(self):
        self.authenticate()
        for nth_board_id in range(1,3):
            nth_board_url = reverse('board-detail', args=[nth_board_id])
        
        expected_data = [self.board1, self.board2, self.board3]
       
        url = reverse("recentlyviewed-list")
        response_data = self.client.get(url).data

        for nth_board_data, expected_board in zip(response_data, expected_data):
            self.assertEqual(nth_board_data['id'], expected_board.id)
