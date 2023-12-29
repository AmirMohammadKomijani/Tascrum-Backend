# from django.http import response
# from rest_framework.test import APITestCase
# from django.test import SimpleTestCase
# from django.urls import reverse , resolve
# from rest_framework import status
# from django.db import IntegrityError
# from rest_framework.test import APIClient
# from datetime import datetime

# from Auth.models import User
# from tascrum.models import *
# from tascrum.views import *

# class CreateItemstViewTest(APITestCase, SimpleTestCase):
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

#         self.board1 = Board.objects.create(
#             title='board test1',
#             backgroundImage = "",
#             workspace=self.workspace
#         )
#         self.board1.members.add(self.members)
#         self.list = List.objects.create(title='List test', board=self.board1)
#         self.card = Card.objects.create(
#             title="card test",
#             list=self.list,
#             startdate='2022-05-15',
#             duedate='2024-05-15',
#             reminder='5 Minuets before'
#         )
#         self.card.members.add(self.members)

#         self.checklist1 = Checklist.objects.create(
#             title= 'checklist1',
#             card= self.card,
#         )
#         self.checklist2 = Checklist.objects.create(
#             title= 'checklist2',
#             card= self.card,
#         )

#         self.item1 = Item.objects.create(
#             content = 'Test Item1',
#             checked =  False,
#             checklist = self.checklist1,
#         )

#         self.item2 = Item.objects.create(
#             content = 'Test Item2',
#             checked =  False,
#             checklist = self.checklist1,
#         )
#         self.item3 = Item.objects.create(
#             content = 'Test Item3',
#             checked =  True,
#             checklist = self.checklist2,
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

#         login_data = {
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('jwt-create'), login_data)

#         self.assertTrue(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data["access"] is not None)

#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')

#     def test_item_url_viewclass(self):
#         url = reverse("critem-list")
#         self.assertEqual(resolve(url).func.cls, CreateItemView)

#     def test_item_url(self):
#         self.authenticate()
#         url = reverse("critem-list")
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_item(self):
#         self.authenticate()
#         url = reverse('critem-list')  
#         data = {
#             'content': 'Test Item4',
#             'checked': False,
#             'checklist': self.checklist2.id,
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         return response

#     def test_item_fields(self):
#         response = self.test_create_item()
#         created_item = Item.objects.get(id=response.data['id'])
#         self.assertEqual(created_item.content, 'Test Item4')
#         self.assertEqual(created_item.checked, False)
#         self.assertEqual(created_item.checklist, self.checklist2)
    
#     def test_item_count(self):
#         self.assertEqual(Item.objects.all().count(), 3)
    
#     # def test_delete_customer_authenticated(self):
#     #     self.authenticate()
#     #     url = reverse('critem-detail', args=[self.item1.pk])
#     #     response = self.client.get(url)
#     #     self.assertEqual(response.status_code, 200)
        
#     # def test_update_item(self):
#     #     self.authenticate()
#     #     item = Item.objects.create(content='Original Item', checked=False, checklist=self.checklist2)

#     #     url = reverse('critem-detail', args=[item.id])

#     #     data = {
#     #         'content': 'Updated Item',
#     #         'checked': True,
#     #     }

#     #     response = self.client.put(url, data, format='json')

#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)

#     #     # item.refresh_from_db()
#     #     # self.assertEqual(item.content, 'Updated Item')
#     #     # self.assertEqual(item.checked, True)
    