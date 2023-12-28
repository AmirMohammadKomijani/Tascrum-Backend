# from django.test import SimpleTestCase,TestCase,Client
# from django.urls import reverse,resolve
# from tascrum.views import WorkspaceView
# from tascrum.models import Workspace
# from Auth.models import User
# from rest_framework import status

# from rest_framework.authtoken.models import Token
# from rest_framework.test import APIClient
# from rest_framework.test import APITestCase



# class TestModels(TestCase):
#     def setUp(self):
#         self.workspace1 = Workspace.objects.create(name = 'workspace test',type = 'small business',
#         description = 'description test',
#         backgroundImage = '')
    
#     def test_workspace_name(self):
#         self.assertEquals(self.workspace1.name,'workspace test')

#     def test_workspace_description(self):
#         self.assertEquals(self.workspace1.description,'description test')

#     def test_workspace_type(self):
#         self.assertEquals(self.workspace1.type,'small business')

#     def test_workspace_backgroundImage(self):
#         self.assertEquals(self.workspace1.backgroundImage,'')

# class TestViews(TestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.workspace_url = reverse('workspace-list')

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

#         login_data = {
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('jwt-create'), login_data)

#         self.assertTrue(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data["access"] is not None)

#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

#     def test_workspace_list_GET_authenticated(self):
#         self.authenticate()
#         response = self.client.get(self.workspace_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

# class TestCreateWorkspaceView(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.workspace_url = reverse('crworkspace-list')

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
#     def test_Create_Workspace_POST(self):
#         # Authenticate the user
#         self.authenticate()

#         create_workspace_data = {
#             'name': 'workspace test2',
#             'type': 'small business',
#             'description': 'description test',
#         }

#         # Send a POST request to create a new workspace
#         response = self.client.post(self.workspace_url, create_workspace_data, format='json')
#         # print(response.content)

#         # Check if the response status code is 201 (Created)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Optionally, you can check the response data for additional details
#         self.assertEqual(response.data['name'], 'workspace test2')
#         self.assertEqual(response.data['type'], 'small business')
#         self.assertEqual(response.data['description'], 'description test')

#         # Optionally, you can check if the new workspace is actually created in the database
#         new_workspace = Workspace.objects.get(name='workspace test2', type='small business', description='description test')
#         self.assertIsNotNone(new_workspace)

#     def test_Update_Workspace_PUT(self):
#         self.authenticate()

#         create_workspace_data = {
#                 'name': 'workspace test2',
#                 'type': 'small business',
#                 'description': 'description test',
#             }

#             # Send a POST request to create a new workspace
#         resp = self.client.post(self.workspace_url, create_workspace_data, format='json')        
#         response=resp.json()
#         id=response['id']

#         data_update={         
#                 'name': 'workspace test2 change',
#                 'type': 'small business',
#                 'description': 'description test change',
#         }
#         url = reverse('crworkspace-detail', kwargs={'pk': id})
#         resp = self.client.put(url, data_update, format='json')
#         self.assertEqual(resp.status_code, 200)

#     def test_Delete_Workspace_DELETE(self):
#         self.authenticate()

#         create_workspace_data = {
#                 'name': 'workspace test2',
#                 'type': 'small business',
#                 'description': 'description test',
#             }
#             # Send a POST request to create a new workspace
#         resp = self.client.post(self.workspace_url, create_workspace_data, format='json')        
#         response=resp.json()
#         id=response['id']

#         url = reverse('crworkspace-detail', kwargs={'pk': id})
#         resp = self.client.delete(url)
#         self.assertEqual(resp.status_code,  status.HTTP_204_NO_CONTENT)

# class TestUrls(APITestCase):

#     def test_workspace_is_resolved(self):
#         url = reverse('workspace-list')
#         self.assertEquals(resolve(url).func.cls, WorkspaceView)

