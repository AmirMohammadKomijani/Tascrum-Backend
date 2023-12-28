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

    def create_list(self, title, board_id):
        create_list_data = {
            'title': title,
            'board': board_id,
        }
        response = self.client.post(self.List_url, create_list_data, format='json')
        return response

    # def test_Update_List_PUT(self):
    #     # Authenticate the user
    #     self.authenticate()

    #     self.workspace = Workspace.objects.create(name='workspace test2', type='small business', description='description test', backgroundImage='')
    #     self.board = Board.objects.create(
    #         title='board test',
    #         backgroundImage="",
    #         workspace=self.workspace
    #     )

    #     # Create a list to update
    #     response_create = self.create_list('List to Update', board_id=self.board.id)

    #     # Ensure the list is created successfully
    #     self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    #     new_list_id = response_create.data['id']

    #     # Define the data you want to use for updating the list
    #     update_list_data = {
    #         'title': 'Updated List',
    #         'board': self.board.id,
    #     }

    #     url = f'/lists/{new_list_id}/'
    #     # print(f'Constructed URL for PUT: {url}')

    #     # Send a PUT request to update the list
    #     response_update = self.client.put(url, update_list_data, format='json')

    #     # Check if the response status code is 200 (OK)
    #     self.assertEqual(response_update.status_code, status.HTTP_200_OK)

    #     # Optionally, you can check the response data for additional details
    #     self.assertEqual(response_update.data['title'], 'Updated List')
    #     self.assertEqual(response_update.data['board'], self.board.id)

    # def test_Delete_List_DELETE(self):
    #     # Authenticate the user
    #     self.authenticate()
    #     self.workspace = Workspace.objects.create(name='workspace test2', type='small business', description='description test', backgroundImage='')
    #     self.board = Board.objects.create(
    #         title='board test',
    #         backgroundImage="",
    #         workspace=self.workspace
    #     )
    #     # Create a list to delete
    #     response_create = self.create_list('List to Delete', board_id=self.board.id)

    #     # Ensure the list is created successfully
    #     self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

    #     new_list_id = response_create.data['id']

    #     # Send a DELETE request to delete the list
    #     response_delete = self.client.delete(f'/lists/{new_list_id}/')

    #     # Check if the response status code is 204 (No Content)
    #     self.assertEqual(response_delete.status_code, status.HTTP_204_NO_CONTENT)

    #     # Optionally, you can check if the list is actually deleted from the database
    #     with self.assertRaises(List.DoesNotExist):
    #         deleted_list = List.objects.get(pk=new_list_id)

class TestUrls(APITestCase):

    def test_List_is_resolved(self):
        url = reverse('list-list')
        self.assertEquals(resolve(url).func.cls, ListView)
    
    def test_Create_List_is_resolved(self):
        url = reverse('crlist-list')
        self.assertEquals(resolve(url).func.cls,CreateListView)
