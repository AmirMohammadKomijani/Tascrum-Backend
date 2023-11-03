from django.test import SimpleTestCase,TestCase,Client
from django.urls import reverse,resolve
from tascrum.views import WorkspaceView
from tascrum.models import Workspace
from Auth.models import User
from rest_framework import status

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework.test import APITestCase



class TestModels(TestCase):
    def setUp(self):
        self.workspace1 = Workspace.objects.create(name = 'workspace test',type = 'small business',
        description = 'description test',
        backgroundImage = '')
    
    def test_workspace_name(self):
        self.assertEquals(self.workspace1.name,'workspace test')

    def test_workspace_description(self):
        self.assertEquals(self.workspace1.description,'description test')

    def test_workspace_type(self):
        self.assertEquals(self.workspace1.type,'small business')

    def test_workspace_backgroundImage(self):
        self.assertEquals(self.workspace1.backgroundImage,'')

class TestViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.workspace_url = reverse('workspace-list')

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

    def test_workspace_list_GET_authenticated(self):
        self.authenticate()
        response = self.client.get(self.workspace_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestUrls(APITestCase):

    def test_workspace_is_resolved(self):
        url = reverse('workspace-list')
        self.assertEquals(resolve(url).func.cls, WorkspaceView)

