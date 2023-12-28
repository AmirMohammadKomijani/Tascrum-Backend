# from django.test import TestCase
# from django.urls import reverse,resolve
# from tascrum.views import ListView,CreateListView
# from tascrum.models import List,Board,Workspace,Member
# from Auth.models import User
# from rest_framework import status
# from rest_framework.test import APIClient
# from rest_framework.test import APITestCase
# from django.http import Http404
# from django.shortcuts import get_object_or_404



# class TestModels(TestCase):
#     def setUp(self):
#         self.workspace = Workspace.objects.create(
#             name='Workspace test',
#             type='small business',
#             description='Workspace description',
#         )
#         self.board = Board.objects.create(title='Board test', workspace=self.workspace)
#         self.list1 = List.objects.create(title='List test', board=self.board)

#     def test_list_name(self):
#         self.assertEqual(self.list1.title, 'List test')

#     def test_list_board(self):
#         self.assertEqual(self.list1.board, self.board)

# class TestViews(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.List_url = reverse('list-list')

#     def authenticate(self):
#         register_data = {
#             'first_name':'test fname',
#             'last_name':'test lname',
#             'username': 'test username',
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('user-list'), register_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # User login
#         login_data = {
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('jwt-create'), login_data)

#         self.assertTrue(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data["access"] is not None)

#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

#     def test_List_list_GET_authenticated(self):
#         self.authenticate()
#         response = self.client.get(self.List_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
    

# class TestCreateList(APITestCase):
    
#     def setUp(self):
#         self.client = APIClient()
#         self.List_url = reverse('crlist-list')

#         self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')
#         self.board = Board.objects.create(
#             title='board test',
#             backgroundImage = "",
#             workspace=self.workspace
#         )

#     def authenticate(self):
#         register_data = {
#             'first_name':'test fname',
#             'last_name':'test lname',
#             'username': 'test username',
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('user-list'), register_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # User login
#         login_data = {
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('jwt-create'), login_data)

#         self.assertTrue(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data["access"] is not None)

#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

#     def test_Create_List_POST(self):
#         # Authenticate the user
#         self.authenticate()

#         # Define the data you want to use for creating a new list
#         create_list_data = {
#             'title': 'New List',
#             'board': self.board.id,  # Assuming you have a board instance available
#         }

#         # Send a POST request to create a new list
#         response = self.client.post(self.List_url, create_list_data, format='json')

#         # Check if the response status code is 201 (Created)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Optionally, you can check the response data for additional details
#         self.assertEqual(response.data['title'], 'New List')
#         self.assertEqual(response.data['board'], self.board.id)

#         # Optionally, you can check if the new list is actually created in the database
#         new_list = List.objects.get(title='New List', board=self.board)
#         self.assertIsNotNone(new_list)

#     def create_list(self, title, board_id):
#         create_list_data = {
#             'title': title,
#             'board': board_id,
#         }
#         response = self.client.post(self.List_url, create_list_data, format='json')
#         return response
    
#     # def test_Update_List_PUT(self):
#     #     self.authenticate()

#     #     create_list_data = {
#     #         'title':'board test',
#     #         'backgroundImage' : "",
#     #         'workspace':self.workspace.id
#     #     }

#     #     resp = self.client.post(reverse('crboard-list'), create_list_data)        
#     #     response=resp.json()
#     #     board_id = response['id']

#     #     create_list_data = {
#     #         'title': 'New List',
#     #         'board': board_id,  # Assuming you have a board instance available
#     #     }
#     #         # Send a POST request to create a new workspace
#     #     resp = self.client.post(self.List_url, create_list_data)        
#     #     response=resp.json()
#     #     id=response['id']
#     #     id_to_update = response.get('id')
    
#     #     # Print debug information
#     #     print(f"Created List ID: {id_to_update}")

#     #     # Check if the list exists before attempting the update
#     #     try:
#     #         list_to_update = get_object_or_404(List, pk=id_to_update)
#     #         print(f"List found before update: {list_to_update}")
#     #     except Http404:
#     #         print(f"List not found with ID: {id_to_update}")

#     #     data_update = {
#     #         'title': 'New List change',
#     #         'board': self.board.id,  # Assuming you have a board instance available
#     #     }

#     #     url = reverse('crlist-detail', kwargs={'pk': id})
#     #     resp = self.client.put(url, data_update)
#     #     self.assertEqual(resp.status_code, 200)


#     # def test_Delete_List_DELETE(self):
#     #     self.authenticate()

#     #     create_list_data = {
#     #         'title': 'New List',
#     #         'board': self.board.id,  # Assuming you have a board instance available
#     #     }
#     #         # Send a POST request to create a new workspace
#     #     resp = self.client.post(self.List_url, create_list_data)        
#     #     response=resp.json()
#     #     id=response['id']

#     #     url = reverse('crlist-detail', kwargs={'pk': id})
#     #     resp = self.client.delete(url)
#     #     self.assertEqual(resp.status_code,  status.HTTP_204_NO_CONTENT)


# class TestUrls(APITestCase):

#     def test_List_is_resolved(self):
#         url = reverse('list-list')
#         self.assertEquals(resolve(url).func.cls, ListView)
    
#     def test_Create_List_is_resolved(self):
#         url = reverse('crlist-list')
#         self.assertEquals(resolve(url).func.cls,CreateListView)
