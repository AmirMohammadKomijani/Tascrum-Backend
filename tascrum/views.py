from django.shortcuts import render
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemberSerializer,WorkspaceSerializer,BoardSerializer,MemberProfileSerializer,CreateWorkspaceSerializer,\
                        CreateBoardSerializer,CreateListSerializer,ListSerializer,CreateCardSerializer,CardSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Member,Workspace,MemberWorkspaceRole,Board,MemberBoardRole,List,Card
from rest_framework.permissions import IsAuthenticated


# Create your views here.


### Profile view
class MemberProfileView(ModelViewSet):
    allowed_methods = ('GET','PUT','HEAD','OPTIONS')
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Member.objects.filter(user_id = self.request.user.id)



### workspace view
class WorkspaceView(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Workspace.objects.filter(members = member_id)

class CreateWorkspaceView(ModelViewSet):
    serializer_class = CreateWorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Workspace.objects.filter(members = member_id)

### board view
class BoardView(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)

class CreateBoardView(ModelViewSet):
    serializer_class = CreateBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)


### List view
class ListView(ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return List.objects.filter(board__in=board_id)

class CreateListView(ModelViewSet):
    serializer_class = CreateListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return List.objects.filter(board__in=board_id)


### Card View
class CardView(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Card.objects.filter(members = member_id)

class CreateCardView(ModelViewSet):
    serializer_class = CreateCardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        (member_id,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Card.objects.filter(members = member_id)



### Home-Account view

class HomeAccountView(ModelViewSet):
    allowed_methods = ('GET','HEAD','OPTIONS')
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Member.objects.filter(user_id = self.request.user.id)