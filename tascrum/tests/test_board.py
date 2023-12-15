from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError
from rest_framework.test import APIClient

from Auth.models import User
from tascrum.models import Member, Board, MemberBoardRole, Workspace
from tascrum.views import BoardViewSet, BoardMembersView, CreateBoardView, BoardImageView, BoardImageView


class BoardViewTest(APITestCase, SimpleTestCase):
    def test_board_url(self):
        url = reverse("board-list")
        self.assertEqual(resolve(url).func.cls, BoardViewSet)

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
    
    def test_count_boards(self):
        previous_board_count = Board.objects.all().count()
        self.authenticate()
        sample_data1 = {"title":'board test1', "backgroundImage":"", "workspace":"1"}
        response = self.client.post(reverse("board-list"), sample_data1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sample_data2 = {"title":'board test2', "backgroundImage":"", "workspace":"1"}
        response = self.client.post(reverse("board-list"), sample_data2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Board.objects.all().count(), previous_board_count+2)

    def test_board_workspace(self):
        self.assertEqual(self.board.workspace , self.workspace)
class CreateBoardViewTest(APITestCase, SimpleTestCase):
    def test_createboard_url(self):
        url = reverse("crboard-list")
        self.assertEqual(resolve(url).func.cls, CreateBoardView)
    
    def setUp(self):
        self.client = APIClient()
        self.board_url = reverse("crboard-list")
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

    def test_create_board(self):
        self.authenticate()
        create_board_data = {"title":'board test3', "backgroundImage":"", "workspace":self.workspace.id}
        response = self.client.post(self.board_url , create_board_data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Board.objects.all().count(), 3)
        # self.assertEqual(Board.objects.filter(title='board test3').count(), 1)

    def test_Update_Board_PUT(self):
        self.authenticate()

        create_board_data = {"title":'board test3', 'has_star':False,"backgroundImage":"", "workspace":self.workspace.id}

            # Send a POST request to create a new workspace
        resp = self.client.post(self.board_url, create_board_data)        
        response=resp.json()
        # print(response)
        id=response['id']

        data_update = {"title":'board test3 change', 'has_star':True, "backgroundImage":"", "workspace":self.workspace.id}

        url = reverse('crboard-detail', kwargs={'pk': id})
        resp = self.client.put(url, data_update)
        # print(resp.content)
        self.assertEqual(resp.status_code, 200)


    def test_Delete_Board_DELETE(self):
        self.authenticate()

        create_board_data = {"title":'board test3', 'has_star':False,"backgroundImage":"", "workspace":self.workspace.id}

            # Send a POST request to create a new workspace
        resp = self.client.post(self.board_url, create_board_data)        
        response=resp.json()
        id=response['id']

        url = reverse('crboard-detail', kwargs={'pk': id})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code,  status.HTTP_204_NO_CONTENT)

    # def test_board_update(self):
    #     self.authenticate()
    #     res = self.client.put(
    #         reverse("crboard-list", kwargs={'id': self.board.id}), {"title": "hi board"})

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    #     updated_todo = Todo.objects.get(id=response.data['id'])
    #     self.assertEqual(updated_todo.is_complete, True)
    #     self.assertEqual(updated_todo.title, 'New one')

class CreateBoardImageViewTest(APITestCase, SimpleTestCase):
    def test_boardimage_url(self):
        url = reverse("board-bgimage-list")
        self.assertEqual(resolve(url).func.cls, BoardImageView)
    
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
            backgroundImage = "hi/hi.png",
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

    def test_boardimage_get_unauthenticated(self):
        url = reverse('board-bgimage-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        return response
    
    def test_boardimage_get_authenticated(self):
        self.authenticate()
        url = reverse('board-bgimage-list') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response

    def test_board_fields_after_get(self):
        response = self.test_boardimage_get_authenticated()
        self.assertEquals(self.board.backgroundImage,'hi/hi.png')

    # def test_boardimage_update(self):
    #     self.authenticate()
    #     url = f'/tascrum/board-bgimage/{self.board.id}/'
    #     print(url)
    #     response = self.client.put(
    #             url,
    #             data={'backgroundImage': "hi/myfile.png"},
    #             format='multipart'
    #         )

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_boardimage_update(self):
    #     self.authenticate()
    #     url = reverse('board-bgimage-list')
    #     image_path = r'E:\saba folder\univercity\term 7 4021\narm\Back-End\media\default_profile.png'
    #     with open(image_path, 'rb') as image_file:
    #         response = self.client.put(
    #                 url,
    #                 data={'backgroundImage': image_file},
    #                 format='multipart'
    #             )

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)