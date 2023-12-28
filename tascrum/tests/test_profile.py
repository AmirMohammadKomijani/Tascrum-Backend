# from django.http import response
# from rest_framework.test import APITestCase
# from django.test import SimpleTestCase
# from django.urls import reverse , resolve
# from rest_framework import status
# from django.db import IntegrityError

# from Auth.models import User
# from tascrum.models import Member
# from tascrum.views import MemberProfileView, ChangePasswordView


# class changepasswordTest(APITestCase , SimpleTestCase):
#     def test_changepassword_url(self):
#         url = reverse("change-list")
#         self.assertEqual(resolve(url).func.cls, ChangePasswordView)

#     def authenticate(self):
#         register_data = {
#             'first_name':'test fname',
#             'last_name':'test lname',
#             'username': 'test username',
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response1 = self.client.post(reverse('user-list'), register_data)
#         self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
#         login_data = {
#             'email': 'fortest@gmail.com',
#             'password': 'Somepass',
#         }
#         response = self.client.post(reverse('jwt-create'), login_data)

#         self.assertTrue(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data["access"] is not None)

#         token = response.data["access"]
#         self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
#         return response1

#     def test_change_password_without_auth(self):
#         response = self.client.post(reverse('change-list') , data={'password': "new_password"})
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

#     def test_change_password_with_auth(self):
#         rep = self.authenticate()
#         response = self.client.post(reverse('change-list') , data={'password': "new_password"})
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



# class ProfileTest(changepasswordTest):
#     def create_member(self):
#         user1 = User.objects.create_user(first_name='saba', last_name='razi',email='razi1.saba@gmail.com',\
#                                           username= "test username", password='thisissaba')
#         self.assertIsInstance(user1 , User)

#         member1 = Member.objects.create(
#             user= user1,
#             occupations='Employee',
#             bio='Another test bio',
#             birthdate='1990-05-15'
#         )

#         self.assertIsInstance(member1 , Member)

#         return member1

#     def test_profile_url(self):
#         url = reverse("profile-list")
#         self.assertEqual(resolve(url).func.cls, MemberProfileView)

#     def test_create_user_for_Member(self):
#         response = User.objects.create_user(first_name='saba', last_name='razi',email='razi.saba@gmail.com',\
#                                           username= "sabarzii", password='thisissaba')
#         self.assertIsInstance(response , User)
#         return response
    
#     def test_create_Member(self):
#         response = Member.objects.create(
#             user=self.test_create_user_for_Member(),
#             occupations='Employee',
#             bio='Another test bio',
#             birthdate='1990-05-15'
#         )

#         self.assertIsInstance(response , Member)
#         return response

#     def test_Meber_fileds(self):
#         member1 = self.create_member()

#         self.assertIsInstance(member1.user, User)
#         self.assertEqual(member1.occupations, 'Employee')
#         self.assertEqual(member1.bio, 'Another test bio')
#         self.assertEqual(str(member1.birthdate), '1990-05-15')

#     # def test_post_profile(self):
#     #     response = self.client.post(reverse("profile-list" , {
#     #         first_name='saba', last_name='razi',email='razi.saba@gmail.com',\
#     #                                       username= "sabarzii", password='thisissaba'
#     #     }))
    
#     # def test_update_profile(self):
#     #     response = self.create_member()
#     #     # response = self.authenticate()
#     #     updated_data = {
#     #         'occupations': 'Student',
#     #         'bio': 'Updated bio',
#     #         'birthdate': '1990-01-01'
#     #     }
#     #     response = self.client.put(
#     #         reverse("profile-list", kwargs={'id': response.data['id']}), {
#     #             "bio": "New one"
#     #         })

#         # response = self.authenticate()

#         # res = self.client.patch(
#         #     reverse("profile-list", kwargs={'id': response.data['id']}), {
#         #         "bio": "New one", 'occupations': "Student"
#         #     })

#         # self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # updated_profile = Member.objects.get(id=response.user.id)
#         # self.assertEqual(updated_profile.occupations, "Student")
#         # self.assertEqual(updated_profile.bio, 'New one')
        