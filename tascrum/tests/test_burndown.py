from django.urls import reverse , resolve
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from datetime import date

from Auth.models import User
from tascrum.models import *
from tascrum.models import Board, Member, BurndownChart, Workspace


class TestBurndownChartModels(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='ali', last_name='samari',email='samari@gmail.com',\
                                          username= "test username", password='Somepass')
        self.member = Member.objects.create(
            user= self.user,
            occupations='Employee',
            bio='Another test bio',
            birthdate='2002-04-18'
        )
        self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')
        self.board = Board.objects.create(
            title='board test',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board.members.add(self.member)
        self.burndown_chart = BurndownChart.objects.create(
            board=self.board,
            member=self.member,
            date=date(2023, 4, 1),
            done=20.5,
            estimate=40.0
        )
    
    def test_burndown_chart_board(self):
        self.assertEquals(self.burndown_chart.board, self.board)
    
    def test_burndown_chart_member(self):
        self.assertEquals(self.burndown_chart.member, self.member)
    
    def test_burndown_chart_date(self):
        self.assertEquals(self.burndown_chart.date.strftime('%Y-%m-%d'), '2023-04-01')
    
    def test_burndown_chart_done(self):
        self.assertEquals(self.burndown_chart.done, 20.5)
        
    def test_burndown_chart_estimate(self):
        self.assertEquals(self.burndown_chart.estimate, 40.0)




class TestBurndownChartViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(first_name='ali', last_name='samari',email='samari@gmail.com',\
                                          username= "test username", password='Somepass')
        self.member = Member.objects.create(
            user= self.user,
            occupations='Employee',
            bio='Another test bio',
            birthdate='2002-04-18'
        )
        self.workspace = Workspace.objects.create(name = 'workspace test2',type = 'small business', description = 'description test', backgroundImage = '')
        self.board = Board.objects.create(
            title='board test',
            backgroundImage = "",
            workspace=self.workspace
        )
        self.board.members.add(self.member)
        self.burndown_chart = BurndownChart.objects.create(
            board=self.board,
            member=self.member,
            date=date.today(),
            done=10.0,
            estimate=20.0
        )

        self.burndown_charts_list_url = reverse('burndown-chart-list')

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

    def test_burndown_charts_list_GET_authenticated(self):
        self.authenticate()
        response = self.client.get(self.burndown_charts_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_burndown_post(self):
        self.authenticate()
        
        burndown_data = {
            "member": self.member.id,
            "board": self.board.id,
            "date": '2023-04-01',
            "done": 5,
            "estimate": 15
        }
        response = self.client.post(self.burndown_charts_list_url, burndown_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_burndown_chart_count(self):
        self.authenticate()
        self.burndown_charts_create_url = reverse('burndown-chart-create-list') + str(self.board.id) + '/create_burndown/'
        burndown_data = {
            "start": '2023-04-01',
            "end": '2023-04-03'
        }
        response = self.client.post(self.burndown_charts_create_url, burndown_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(BurndownChart.objects.count(), 3)

        self.assertEqual(BurndownChart.objects.filter(board=self.board).count(), 3)
