from django.http import response
from rest_framework.test import APITestCase
from django.test import SimpleTestCase
from django.urls import reverse , resolve
from rest_framework import status
from django.db import IntegrityError


from Auth.models import User
from tascrum.models import Member, Board, MemberBoardRole
from tascrum.views import BoardView, BoardMembersView, CreateBoardView, BoardImageView


class BoardTest(APITestCase, SimpleTestCase):
    
    def test_profile_url(self):
        url = reverse("board-list")
        self.assertEqual(resolve(url).func.cls, BoardView)

    def test_changepassword_url(self):
        url = reverse("crboard-list")
        self.assertEqual(resolve(url).func.cls, CreateBoardView)
    
    

    # def test_create_user_for_Member(self):
    #     response = User.objects.create_user(first_name='saba', last_name='razi',email='razi.saba@gmail.com',\
    #                                       username= "sabarzii", password='thisissaba')
    #     self.assertIsInstance(response , User)
    #     return response
    
    # def test_create_Member(self):
    #     response = Member.objects.create(
    #         user=self.test_create_user_for_Member(),
    #         occupations='Employee',
    #         bio='Another test bio',
    #         birthdate='1990-05-15'
    #     )

    #     self.assertIsInstance(response , Member)
    #     return response

    # def test_Meber_fileds(self):

    #     user1 = User.objects.create_user(first_name='saba', last_name='razi',email='razi1.saba@gmail.com',\
    #                                       username= "sabarzii1", password='thisissaba')
    #     self.assertIsInstance(user1 , User)

    #     member1 = Member.objects.create(
    #         user= user1,
    #         occupations='Employee',
    #         bio='Another test bio',
    #         birthdate='1990-05-15'
    #     )

    #     self.assertIsInstance(member1 , Member)

    #     self.assertEqual(member1.user, user1)
    #     self.assertEqual(member1.occupations, 'Employee')
    #     self.assertEqual(member1.bio, 'Another test bio')
    #     self.assertEqual(str(member1.birthdate), '1990-05-15')
