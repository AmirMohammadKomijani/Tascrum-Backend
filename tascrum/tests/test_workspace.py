from django.test import SimpleTestCase,TestCase,Client
from django.urls import reverse,resolve
from tascrum.views import WorkspaceView
from tascrum.models import Workspace
from Auth.models import User
from rest_framework.authtoken.models import Token  # Import Token model if using token-based authentication
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
        # self.user = User.objects.create(username='testuser', password='testpassword')
        # self.token = Token.objects.create(user=self.user)
        # self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.workspace_url = reverse('workspace-list')
    
    def create_authenticated_client(self):
        # Create a user and obtain an authentication token
        user = User.objects.create(username='testuser', password='testpassword')
        token, created = Token.objects.get_or_create(user=user)

        # Create an authenticated client with the token
        client = Client()
        client.defaults(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client
    
    def test_workspace_list_GET(self):
        response = self.client.get(self.workspace_url)
        self.assertEquals(response.status_code,200)

class TestUrls(APITestCase):

    def test_workspace_is_resolved(self):
        # Use the namespace to reverse the URL
        url = reverse('workspace-list')
        self.assertEquals(resolve(url).func.cls, WorkspaceView)

