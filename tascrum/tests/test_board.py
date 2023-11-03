from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APIClient

from Auth.models import User
from tascrum.models import Member, Board, MemberBoardRole, Workspace
from tascrum.views import BoardView, BoardMembersView, CreateBoardView, BoardImageView


class BoardViewTest(APITestCase, SimpleTestCase):
    def test_profile_url(self):
        url = reverse("board-list")
        self.assertEqual(resolve(url).func.cls, BoardView)
    def test_kill(self):
        self.assertEqual("hi","hi")
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
        self.board = Board.objects.create(
            title='board test',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board.members.add(self.members)

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

    def test_board_fields(self):
        self.assertEquals(self.board.title,'board test')
        self.assertEquals(self.board.backgroundImage,'')

    def test_board_get_authenticated(self):
        self.authenticate()
        url = reverse('board-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_board_fields_after_get(self):
        response = self.test_board_get_authenticated()
        self.assertEquals(self.board.title,'board test')
        self.assertEquals(self.board.backgroundImage,'')

    def test_board_get_unauthenticated(self):
        url = reverse('board-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        return response

class CreateBoardViewTest(APITestCase, SimpleTestCase):
    def test_changepassword_url(self):
        url = reverse("crboard-list")
        self.assertEqual(resolve(url).func.cls, CreateBoardView)
    
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
        self.board = Board.objects.create(
            title='board test',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board.members.add(self.members)

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

    # def test_create_board(self):
    #     self.authenticate()
    #     board_data = {
    #         "title": "New Board",
    #         "workspace": self.workspace.name,
    #         "backgroundImage": "image-url"
    #     }

    #     url = reverse('crboard-list') 
    #     response = self.client.post(url, board_data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     self.assertEqual(Board.objects.filter(members=self.member, title='New Board Title').count(), 1)

    # def test_board_update(self):
    #     self.authenticate()
    #     res = self.client.put(
    #         reverse("crboard-list", kwargs={'id': self.board.id}), {
    #             "title": "New one"
    #         })

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    #     updated_todo = Todo.objects.get(id=response.data['id'])
    #     self.assertEqual(updated_todo.is_complete, True)
    #     self.assertEqual(updated_todo.title, 'New one')

