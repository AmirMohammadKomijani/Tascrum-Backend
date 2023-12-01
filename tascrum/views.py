from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework import status
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ModelViewSet
from .models import *
from Auth.models import User
from .utils import generate_invitation_link
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django.shortcuts import get_object_or_404
from collections import defaultdict

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
    
    def perform_create(self, serializer):
        board = serializer.save()
        invitation_link = generate_invitation_link()
        board.invitation_link = invitation_link
        board.save()
        Lable.objects.create(board=board, color='#e67c73', title='')
        Lable.objects.create(board=board, color='#f7cb4d', title='')
        Lable.objects.create(board=board, color='#41b375', title='')
        Lable.objects.create(board=board, color='#7baaf7', title='')
        Lable.objects.create(board=board, color='#ba67c8', title='')
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
    serializer_class = CreateBoardStarSerializer

    @action(detail=True, methods=['put'])
    def update_star(self, request, pk=None):
        board = self.get_object()
        serializer = self.get_serializer(board, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class BoardInvitationLinkView(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardInviteLink

    def get_invitation_link(self, request):
        board_id = request.GET.get('board_id')
        invitation_link = Board.objects.get(id=board_id).invitation_link
        return HttpResponse(invitation_link)
    
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


    def get_serializer_context(self):
        return {'user_id':self.request.user.id}


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

## Label in Board
class CreateLabelView(ModelViewSet):
    serializer_class = CreateLabelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        board_id = Board.objects.filter(members = member_id)
        return Lable.objects.filter(board__in=board_id)

class LabelBoardView(ModelViewSet):
    serializer_class = LabelBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        return Board.objects.filter(id=board_id)


# assign Labels to card
class LabelCardAssignView(ModelViewSet):
    queryset = CardLabel.objects.all()
    serializer_class = LabelCardAssignSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

class LabelCardView(ModelViewSet):
    serializer_class = LabelCardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        card_id = self.kwargs.get('pk')
        # labels_in_card = CardLabel.objects.filter(card = card_id).all()
        # cards = labels_in_card.values_list('label__card_id',flat=True)
        # return Card.objects.exclude(id__in = cards).all()
        return Card.objects.filter(id = card_id)

        # board_id = self.request.query_params.get('board')
        # members_in_board =  MemberBoardRole.objects.filter(board=board_id).all()
        # members = members_in_board.values_list('member__user_id', flat=True)
        # return User.objects.exclude(id__in = members).all()

### invite member
class FindUserView(ModelViewSet):
    serializer_class = FindUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username','email']

    def get_queryset(self):
        board_id = self.request.query_params.get('board')
        members_in_board =  MemberBoardRole.objects.filter(board=board_id).all()
        members = members_in_board.values_list('member__user_id', flat=True)
        return User.objects.exclude(id__in = members).all()

class InviteMemberView(ModelViewSet):
    serializer_class = AddMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return MemberBoardRole.objects.filter(member=member_id)

### Home-Account view

class HomeAccountView(ModelViewSet):
    allowed_methods = ('GET','HEAD','OPTIONS')
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Member.objects.filter(user_id = self.request.user.id)

### Drag and Drop

class Internal_DndView(ModelViewSet):
    serializer_class = Internal_DnDSerializer

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Card.objects.filter(members = member)


### time line 
class ListTimelineView(ModelViewSet):
    serializer_class = ListTimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        return Board.objects.filter(id=board_id)

class MemberTimelineView(ModelViewSet):
    serializer_class = MembersTimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        return Board.objects.filter(id = board_id)

class LabelTimelineView(ModelViewSet):
    serializer_class = LabelsTimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        return Board.objects.filter(id = board_id)



### Calender View

class CalenderView(ModelViewSet):
    serializer_class = CalenderSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['startdate','duedate','reminder','storypoint','setestimate']


    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        boards = Board.objects.filter(members = member)
        lists = List.objects.filter(board__in = boards)
        return Card.objects.filter(list__in=lists)



class CreateBurndownChartView(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id}
    def get_queryset(self):
        return BurndownChart.objects.filter(user = self.request.user.id)
  
    
class BurndownChartViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user.id
        return BurndownChart.objects.filter(board__members=user)
    
    def list(self, request, *args, **kwargs): 
        queryset = self.filter_queryset(self.get_queryset()) 
        serializer = self.get_serializer(queryset, many=True) 
        data = defaultdict(list) 
        for item in serializer.data: 
            data[item['date']].append(item['data'][0]) 
        return Response([{'id': i+1, 'date': k, 'data': v} for i, (k, v) in enumerate(data.items())]) 
    
    def update(self, request, *args, **kwargs):
        date = request.data.get('date')
        member_id = request.data.get('member')
        burndown_chart = self.get_queryset().filter(date=date, member__id=member_id).first()
        if burndown_chart is None:
            return Response({'error': 'No matching BurndownChart found.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(burndown_chart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BurndownChartSumViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, board_id=None, member_id=None):
        queryset = BurndownChart.objects.filter(board__id=board_id, member__id=member_id)
        done_sum = queryset.aggregate(Sum('done'))['done__sum']
        estimate_sum = queryset.aggregate(Sum('estimate'))['estimate__sum']
        return Response({'done_sum': done_sum, 'estimate_sum': estimate_sum})
    