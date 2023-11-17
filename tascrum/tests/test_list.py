from django.test import TestCase
from django.urls import reverse,resolve
from tascrum.views import ListView,CreateListView
from tascrum.models import List,Board,Workspace,Member
from Auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase



class TestModels(TestCase):
    def setUp(self):
        self.workspace = Workspace.objects.create(
            name='Workspace test',
            type='small business',
            description='Workspace description',
        )
        self.board = Board.objects.create(title='Board test', workspace=self.workspace)
        self.list1 = List.objects.create(title='List test', board=self.board)

    def test_list_name(self):
        self.assertEqual(self.list1.title, 'List test')

    def test_list_board(self):
        self.assertEqual(self.list1.board, self.board)

class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.List_url = reverse('list-list')

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

    def test_List_list_GET_authenticated(self):
        self.authenticate()
        response = self.client.get(self.List_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_Create_List_POST(self):
    #     # Authenticate the user
    #     self.authenticate()

    #     # Define the data you want to use for creating a new list
    #     create_list_data = {
    #         'title': 'New List',
    #         'board': self.board,  # Assuming you have a board instance available
    #     }

    #     # Send a POST request to create a new list
    #     response = self.client.post(self.List_url, create_list_data, format='json')

    #     # Check if the response status code is 201 (Created)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     # Optionally, you can check the response data for additional details
    #     self.assertEqual(response.data['title'], 'New List')
    #     self.assertEqual(response.data['board'], self.board.id)

    #     # Optionally, you can check if the new list is actually created in the database
    #     new_list = List.objects.get(title='New List', board=self.board)
    #     self.assertIsNotNone(new_list)

class TestCreateList(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.List_url = reverse('crlist-list')

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

    def test_Create_List_POST(self):
        # Authenticate the user
        self.authenticate()

        self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')
        self.board = Board.objects.create(
            title='board test',
            backgroundImage = "",
            workspace=self.workspace
        )

        # Define the data you want to use for creating a new list
        create_list_data = {
            'title': 'New List',
            'board': self.board.id,  # Assuming you have a board instance available
        }

        # Send a POST request to create a new list
        response = self.client.post(self.List_url, create_list_data, format='json')

        # Check if the response status code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Optionally, you can check the response data for additional details
        self.assertEqual(response.data['title'], 'New List')
        self.assertEqual(response.data['board'], self.board.id)

        # Optionally, you can check if the new list is actually created in the database
        new_list = List.objects.get(title='New List', board=self.board)
        self.assertIsNotNone(new_list)

class TestUrls(APITestCase):

    def test_List_is_resolved(self):
        url = reverse('list-list')
        self.assertEquals(resolve(url).func.cls, ListView)
    
    def test_Create_List_is_resolved(self):
        url = reverse('crlist-list')
        self.assertEquals(resolve(url).func.cls,CreateListView)


# class CreateListViewsTest(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         user1 = User.objects.create_user(first_name='saba', last_name='razi',email='razi1.saba@gmail.com',\
#                                           username= "test username", password='thisissaba')
#         self.members = Member.objects.create(
#             user= user1,
#             occupations='Employee',
#             bio='Another test bio',
#             birthdate='1990-05-15'
#         )
#         self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')
#         self.board = Board.objects.create(
#             title='board test',
#             backgroundImage = "",
#             workspace=self.workspace
#         )
#         self.board.members.add(self.members)
#         self.list = List.objects.create(title='List test', board=self.board)