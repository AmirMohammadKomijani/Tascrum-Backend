from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
# from django_filters import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from .serializers import MemberSerializer,WorkspaceSerializer,BoardSerializer,MemberProfileSerializer,CreateWorkspaceSerializer,\
                        CreateBoardSerializer,CreateListSerializer,ListSerializer,CreateCardSerializer,CardSerializer,\
                            CardAssignSerializer,ChangePasswordSerializer,AddMemberSerializer,FindUserSerializer,BoardMembersSerializer,\
                            BoardBackgroundImageSerializer,BoardStarSerializer,\
                            BoardRecentlyViewed,CreateItemSerializer,ChecklistSerializer,CreateChecklistSerializer,CreateLabelSerializer,LabelSerializer,\
                                Internal_DnDSerializer,CardChecklistsSerializer, LabelBoardSerializer,CreateBoardStarSerializer
from rest_framework.viewsets import ModelViewSet
from .models import *
from Auth.models import User
# from .utils import generate_invitation_link
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

# Create your views here.


### Profile view
class MemberProfileView(ModelViewSet):
    allowed_methods = ('GET','PUT','HEAD','OPTIONS')
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Member.objects.filter(user_id = self.request.user.id)


class ChangePasswordView(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        user = self.request.user.id
        return User.objects.filter(id = user)



### workspace view
class WorkspaceView(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Workspace.objects.filter(members = member_id)

class CreateWorkspaceView(ModelViewSet):
    serializer_class = CreateWorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Workspace.objects.filter(members = member_id)

### board view
class BoardView(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)
    
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     for instance in queryset:
    #         instance.lastseen = datetime.now()
    #         instance.save()

    #     return super(BoardView, self).list(request, *args, **kwargs)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.lastseen = datetime.now()
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
class BoardImageView(ModelViewSet):
    serializer_class = BoardBackgroundImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)

class CreateBoardView(ModelViewSet):
    serializer_class = CreateBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    
    # def perform_create(self, serializer):
    #     board = serializer.save()
        
    #     # Generate the invitation link
    #     invitation_link = generate_invitation_link()
        
    #     # Assign the invitation link to the board
    #     board.invitation_link = invitation_link
    #     board.save()

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)


class BoardMembersView(ModelViewSet):
    serializer_class = BoardMembersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id)
    
class BoardStarView(ModelViewSet):
    serializer_class = BoardStarSerializer
    
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members=member_id, has_star=True)
    
class BoardStarUpdate(ModelViewSet):
    # queryset = Board.objects.all()
    serializer_class = CreateBoardStarSerializer

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member)

    # @action(detail=True, methods=['put'])
    # def update_star(self, request, pk=None):
    #     board = self.get_object()
    #     serializer = self.get_serializer(board, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


class BoardRecentlyViewedView(ModelViewSet):
    serializer_class = BoardRecentlyViewed
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members = member_id).order_by('-lastseen')[:3]
        
### List view
class ListView(ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return List.objects.filter(board__in=board_id)

class CreateListView(ModelViewSet):
    serializer_class = CreateListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return List.objects.filter(board__in=board_id)


### Card View
class CardView(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = self.request.query_params.get('board')
        list_id = List.objects.filter(board__in = board_id)
        return Card.objects.filter(list__in=list_id)

class CreateCardView(ModelViewSet):
    serializer_class = CreateCardSerializer
    permission_classes = [IsAuthenticated]
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Card.objects.filter(members = member_id)

class CardAssignmentView(ModelViewSet):
    queryset = MemberCardRole.objects.all()
    serializer_class = CardAssignSerializer
    permission_classes = [IsAuthenticated]
    # allowed_methods = ('GET','DELETE','POST','HEAD','OPTIONS')


    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

    # def get_queryset(self):
    #     member_id = Member.objects.get(user_id = self.request.user.id)
    #     return MemberCardRole.objects.filter(member=member_id)


## Checklist in card view
class CreateItemView(ModelViewSet):
    serializer_class = CreateItemSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        card_id = Card.objects.filter(members = member_id)
        checklist_id = Checklist.objects.filter(card__in= card_id)
        return Item.objects.filter(checklist__in=checklist_id)

class ChecklistView(ModelViewSet):
    serializer_class = ChecklistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # member_id = Member.objects.get(user_id = self.request.user.id)
        card_id = self.kwargs.get('pk')
        return Checklist.objects.filter(card__in=card_id)

class CardChecklistView(ModelViewSet):
    serializer_class = CardChecklistsSerializer

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Card.objects.filter(members=member)

class CreateChecklistView(ModelViewSet):
    serializer_class = CreateChecklistSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        card_id = Card.objects.filter(members = member_id)
        return Checklist.objects.filter(card__in=card_id)

## Label in Card
class CreateLabelView(ModelViewSet):
    serializer_class = CreateLabelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return Lable.objects.filter(board__in=board_id)

class LabelView(ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return Lable.objects.filter(board__in=board_id)

class LabelBoardView(ModelViewSet):
    serializer_class = LabelBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Board.objects.filter(members=member)

### invite member

class FindUserView(ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = FindUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username','email']

    # def get_serializer_context(self):
    #     return {'user_id':self.request.user.id}

    def get_queryset(self):
        # queryset = User.objects.all()
        # member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = self.request.query_params.get('board')
        members_in_board =  MemberBoardRole.objects.filter(board=board_id).all()
        members = members_in_board.values_list('member__user_id', flat=True)
        return User.objects.exclude(id__in = members).all()
        
        # return User.objects.filter(Q(id__in = members_bo))
        # members_in_board = board.members.all()
        # queryset = queryset.exclude(Q(users__in=members_in_board) | Q(member__in=members_in_board))
        # return queryset


class InviteMemberView(ModelViewSet):
    serializer_class = AddMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return MemberBoardRole.objects.filter(member=member_id)

    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     board_id = serializer.validated_data['board']
    #     owner = Member.objects.get(user_id=self.request.user.id)

    #     # Check if the owner has the role of "owner" for the board
    #     board_role = MemberBoardRole.objects.filter(member=owner, board=board_id).first()
        
    #     if board_role and board_role.role == "owner":
    #         for member_id in serializer.validated_data['member']:
    #             # Check if the member is already part of this board
    #             # if not MemberBoardRole.objects.filter(member=member_id, board=board_id).exists():
    #             MemberBoardRole.objects.create(member=member_id, board=board_id, role='member')
    #         #     else:
    #         #         return Response({"detail": f"Member {member_id} is already part of this board."}, status=status.HTTP_400_BAD_REQUEST)
    #         # return Response({"detail": "Members have been added to the board."}, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response({"detail": "You are not the owner of this board."}, status=status.HTTP_403_FORBIDDEN)




### Home-Account view

class HomeAccountView(ModelViewSet):
    allowed_methods = ('GET','HEAD','OPTIONS')
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Member.objects.filter(user_id = self.request.user.id)


### burndown chart

# class CreateBurndownChartView(ModelViewSet):
#     serializer_class = CreateBurndownChartSerializer
#     permission_classes = [IsAuthenticated]

#     def get_serializer_context(self):
#         return {'user_id':self.request.user.id}
#     def get_queryset(self):
#         return BurndownChart.objects.filter(user = self.request.user.id)


### Drag and Drop

class Internal_DndView(ModelViewSet):
    serializer_class = Internal_DnDSerializer

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Card.objects.filter(members = member)