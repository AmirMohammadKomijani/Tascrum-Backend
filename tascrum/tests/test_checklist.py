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

class CreateChecklistViewTest(APITestCase, SimpleTestCase):
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
        self.list = List.objects.create(title='List test', board=self.board1)
        self.card = Card.objects.create(
            title="card test",
            list=self.list,
            startdate='2022-05-15',
            duedate='2024-05-15',
            reminder='5 Minuets before'
        )
        self.card.members.add(self.members)

        self.checklist1 = Checklist.objects.create(
            title= 'checklist1',
            card= self.card,
        )
        self.checklist2 = Checklist.objects.create(
            title= 'checklist2',
            card= self.card,
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

        login_data = {
            'email': 'fortest@gmail.com',
            'password': 'Somepass',
        }
        response = self.client.post(reverse('jwt-create'), login_data)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["access"] is not None)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_crchecklist_url_viewclass(self):
        url = reverse("crchecklist-list")
        self.assertEqual(resolve(url).func.cls, CreateChecklistView)

    def test_checklistview_url(self):
        self.authenticate()
        url = reverse("crchecklist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_checklist(self):
        self.authenticate()
        url = reverse('crchecklist-list')  

        data = {
            'title': 'New Checklist',
            'card': self.card.id,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_checklist_fields(self):
        response = self.test_create_checklist()
        checklist_id = response.data['id']
        checklist = Checklist.objects.get(id=checklist_id)

        self.assertEqual(checklist.title, 'New Checklist')
        self.assertEqual(checklist.card, self.card)

    def test_checkllist_count(self):
        self.assertEqual(Checklist.objects.all().count(), 2)
    
    # def test_update_checklist(self):
    #     self.authenticate()
    #     url = reverse('crchecklist-list')  

    #     data = {
    #         'title': 'New Checklist',
    #         'card': self.card.id,
    #     }

    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     url = reverse('crchecklist-detail', kwargs={'pk': response.data['id']})

    #     data = {
    #         'title': 'Updated Title',
    #     }

    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     checklist.refresh_from_db()

    #     self.assertEqual(checklist.title, 'Updated Title')

class CardChecklistViewTest(APITestCase):
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
        self.list = List.objects.create(title='List test', board=self.board1)
        self.card = Card.objects.create(
            title="card test",
            list=self.list,
            startdate='2022-05-15',
            duedate='2024-05-15',
            reminder='5 Minuets before'
        )
        self.card.members.add(self.members)

        self.checklist1 = Checklist.objects.create(
            title= 'checklist1',
            card= self.card,
        )
        self.checklist2 = Checklist.objects.create(
            title= 'checklist2',
            card= self.card,
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

        login_data = {
            'email': 'fortest@gmail.com',
            'password': 'Somepass',
        }
        response = self.client.post(reverse('jwt-create'), login_data)

        self.assertTrue(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["access"] is not None)

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

    def test_checklist_url_viewclass(self):
        url = reverse("checklist-list")
        self.assertEqual(resolve(url).func.cls, CardChecklistView)

    def test_card_checklist_url(self):
        self.authenticate()
        url = reverse("checklist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

