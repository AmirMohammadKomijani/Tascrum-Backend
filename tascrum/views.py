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
from .utils import generate_invitation_link,OPENAI_API_KEY
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.db.models import Sum, F
from datetime import datetime, timedelta
import csv
import webcolors
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from rest_framework.views import APIView
# import webcolors
# Create your views here.
import django_filters
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter, DateTimeFilter

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

class WorkspaceMembersView(ModelViewSet):
    serializer_class = WorkspaceMembersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Workspace.objects.filter(id = self.kwargs['workspace_pk'],members = member_id)

### board view
class BoardViewSet(ModelViewSet):
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
    # allowed_methods = ('POST','HEAD','OPTIONS')
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

class TimelineStartPeriodView(ModelViewSet):
    serializer_class = TimelineStartSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        boards = Board.objects.filter(id = self.kwargs['board_pk'],members = member)
        lists = List.objects.filter(board__in = boards)
        cards = Card.objects.filter(list__in=lists, startdate__isnull=False) 
        return [cards.order_by('startdate').first()]

class TimelineDuePeriodView(ModelViewSet):
    serializer_class = TimelineDueSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        boards = Board.objects.filter(id = self.kwargs['board_pk'],members = member)
        lists = List.objects.filter(board__in = boards)
        cards = Card.objects.filter(list__in=lists, duedate__isnull=False) 
        return [cards.order_by('duedate').last()]


### Meeting View
class CreateMeetingView(ModelViewSet):
    serializer_class = CreateMeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id':self.request.user.id,'board_id' : self.kwargs['board_pk']}

    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        return Meeting.objects.filter(member = member,board=self.kwargs['board_pk'])

class MeetingView(ModelViewSet):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        # member = Member.objects.get(user_id = self.request.user.id)
        return Member.objects.filter(user_id = self.request.user.id,bmembers=self.kwargs['board_pk'])

### Calender View

class CalenderView(ModelViewSet):
    serializer_class = CalenderSerializer
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['startdate','duedate','reminder','storypoint','setestimate']


    def get_queryset(self):
        member = Member.objects.get(user_id = self.request.user.id)
        boards = Board.objects.filter(id = self.kwargs['board_pk'],members = member)
        lists = List.objects.filter(board__in = boards)
        return Card.objects.filter(list__in=lists)

### chatbot
# class CardCSVViewSet(ModelViewSet):
#     queryset = Card.objects.all()
#     serializer_class = CardChatbotSerializer  
    
#     @staticmethod
#     def closest_colour(hex_color):
#         requested_colour = webcolors.hex_to_rgb(hex_color)
#         min_colours = {}
#         for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
#             r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#             rd = (r_c - requested_colour[0]) ** 2
#             gd = (g_c - requested_colour[1]) ** 2
#             bd = (b_c - requested_colour[2]) ** 2
#             min_colours[(rd + gd + bd)] = name
#         return min_colours[min(min_colours.keys())]
#     @staticmethod
#     def get_colour_name(requested_colour):
#         try:
#             closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
#         except ValueError:
#             closest_name = closest_colour(requested_colour)
#             actual_name = None
#         return actual_name, closest_name
    
#     def export_csv(self):
#         number = self.kwargs.get('pk')
#         file_path=f'./media/csv/{number}.csv'
#         lists = List.objects.filter(board=number)
#         queryset = Card.objects.filter(list__in = lists)
#         serializer = CardChatbotSerializer(queryset, many=True)

#         with open(file_path, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             keys = [
#                         'title of card',
#                         'list of the card',
#                         'members of card',
#                         'labels of card',
#                         'start date of card',
#                         'due date of card',
#                         'reminder of card',
#                         'storypoint of card',
#                         'estimate of card',
#                         'description of card',
#                         'status of card'
#                         ]
#             writer.writerow(keys)

#             for row in serializer.data:
#                 members_value = ', '.join([member.get('user', {}).get('username', '') for member in row.get('members', [])])
#                 labels_value = [
#                         {'title': label.get('title', ''), 'color': self.closest_colour(label.get('color', ''))}
#                         for label in row.get('labels', [])
#                     ]                
                    
#                 writer.writerow([
#                     row.get('title', ''),
#                     row.get('list', {}).get('title', ''),
#                     members_value,
#                     labels_value,
#                     row.get('startdate', ''),
#                     row.get('duedate', ''),
#                     row.get('reminder', ''),
#                     row.get('storypoint', ''),
#                     row.get('setestimate', ''),
#                     row.get('description', ''),
#                     row.get('status', ''),
#                 ])

#     def get_queryset(self):
#         self.export_csv()
#         member_id = Member.objects.get(user_id = self.request.user.id)
#         return Card.objects.filter(members = member_id)

# class ChatbotAPIView(ModelViewSet):
#     queryset = Chatbot.objects.all()
#     serializer_class = ChatbotRequestSerializer
#     # @staticmethod
#     def get_answer(self, number, request_message):
#         agent = create_csv_agent(
#         ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY),
#         f"./media/csv/{number}.csv",
#         verbose=True,
#         agent_type=AgentType.OPENAI_FUNCTIONS,)

#         return agent.run(request_message)

#     def post(self, request, *args, **kwargs):
#         serializer = ChatbotRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         request_message = serializer.validated_data.get('request_message')

#         answer = self.get_answer(self.kwargs.get('pk'), request_message).replace("dataframe" , 'board')
#         response_data = {"ai_message": answer}

#         return Response(response_data)
    
#     def get_queryset(self):
#         return Chatbot.objects.none()
  
### Burndown Chart View    
class BurndownChartViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        user = self.request.user.id
        return BurndownChart.objects.filter(board_id=board_id,board__members=user).order_by('date', 'member__id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actuall_remaining = total_estimate

        serializer = self.get_serializer(queryset, many=True)
        data = defaultdict(list)

        for item in serializer.data:
            data[item['date']].append(item['data'][0])

        response_data = []
        running_done_total = 0

        for date, items in data.items():
            done_sum = 0
            estimate_sum = 0
            processed_items = []
            for item in items:
                out_of_estimate = item['estimate'] - item['done']
                item['out_of_estimate'] = out_of_estimate
                done_sum += item['done']
                estimate_sum += item['estimate']
                processed_items.append(item) 
            running_done_total += done_sum
            date_dict = {
                'date': date,
                'data': sorted(processed_items, key=lambda x: x['member']),
                'done_sum': done_sum,
                'estimate_sum': estimate_sum,
                'act_rem': actuall_remaining - running_done_total,
                'est_rem': total_estimate - estimate_sum
            }
            response_data.append(date_dict)
            total_estimate -= estimate_sum 

        return Response(response_data)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actuall_remaining = total_estimate

        serializer = self.get_serializer(queryset, many=True)
        data = defaultdict(list)

        for item in serializer.data:
            data[item['date']].append(item['data'][0])

        response_data = []
        running_done_total = 0

        for date, items in data.items():
            done_sum = 0
            estimate_sum = 0
            processed_items = []
            for item in items:
                out_of_estimate = item['estimate'] - item['done']
                item['out_of_estimate'] = out_of_estimate
                done_sum += item['done']
                estimate_sum += item['estimate']
                processed_items.append(item)  
            running_done_total += done_sum
            date_dict = {
                'date': date,
                'data': sorted(processed_items, key=lambda x: x['member']),
                'done_sum': done_sum,
                'estimate_sum': estimate_sum,
                'act_rem': actuall_remaining - running_done_total,
                'est_rem': total_estimate - estimate_sum
            }
            response_data.append(date_dict)
            total_estimate -= estimate_sum 

        return Response(response_data)

    def update(self, request, *args, **kwargs):
        date = request.data.get('date')
        member_id = request.data.get('member')
        burndown_chart = self.get_queryset().filter(date=date, member_id=member_id).first()

        if burndown_chart is None:
            return Response({'error': 'No matching BurndownChart found.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(burndown_chart, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    
    

    def list(self, request, *args, **kwargs):
        board_id = self.kwargs.get('board_id', None)
        queryset = BurndownChart.objects.filter(board__id=board_id).values(
            'member'
        ).annotate(
            done_sum=Sum('done'),
            estimate_sum=Sum('estimate'),
            out_of_estimate_sum=Sum(F('estimate') - F('done'))  
        ).order_by('member')
        overall_done_sum = queryset.aggregate(Sum('done_sum'))['done_sum__sum'] or 0
        overall_estimate_sum = queryset.aggregate(Sum('estimate_sum'))['estimate_sum__sum'] or 0
        members_data = list(queryset)  

        response_data = {
            'members': members_data,
            'done_total_sum': overall_done_sum,
            'estimate_total_sum': overall_estimate_sum,
        }

        return Response(response_data)
    
    

class BurndownChartSumViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        board_id = self.kwargs.get('board_id', None)
        queryset = BurndownChart.objects.filter(board__id=board_id).values(
            'member'
        ).annotate(
            done_sum=Sum('done'),
            estimate_sum=Sum('estimate'),
            out_of_estimate_sum=Sum(F('estimate') - F('done'))  
        ).order_by('member')
        overall_done_sum = queryset.aggregate(Sum('done_sum'))['done_sum__sum'] or 0
        overall_estimate_sum = queryset.aggregate(Sum('estimate_sum'))['estimate_sum__sum'] or 0
        members_data = list(queryset)  

        response_data = {
            'members': members_data,
            'done_total_sum': overall_done_sum,
            'estimate_total_sum': overall_estimate_sum,
        }

        return Response(response_data)

class BurndownCreateView(ModelViewSet):
    queryset = BurndownChart.objects.all()
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def create_burndown(self, request, pk=None):
        board = get_object_or_404(Board, pk=pk)
        BurndownChart.objects.filter(board=board).delete()
        data = request.data
        start_date = datetime.strptime(data['start'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end'], '%Y-%m-%d').date()
        if start_date > end_date:
            return Response({'error': 'Start date must be before end date.'}, status=status.HTTP_400_BAD_REQUEST)
        members = board.members.all()
        for current_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days + 1)):
            for member in members:
                burndown_data = {
                    'board': board.id,
                    'member': member.id,
                    'date': current_date,
                    'done': 0,
                    'estimate': 0
                }
                serializer = self.get_serializer(data=burndown_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)

        return Response({"message": "Burndown chart created successfully"}, status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        serializer.save()


class BurndownChartEstimateViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        user = self.request.user.id
        return BurndownChart.objects.filter(board_id=board_id,board__members=user).order_by('date', 'member__id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actuall_remaining = total_estimate

        serializer = self.get_serializer(queryset, many=True)
        data = defaultdict(list)

        for item in serializer.data:
            data[item['date']].append(item['data'][0])

        response_data = []
        running_done_total = 0

        for date, items in data.items():
            done_sum = 0
            estimate_sum = 0
            processed_items = []
            for item in items:
                out_of_estimate = item['estimate'] - item['done']
                item['out_of_estimate'] = out_of_estimate
                done_sum += item['done']
                estimate_sum += item['estimate']
                processed_items.append(item) 
            running_done_total += done_sum
            date_dict = {
                'date': date,
                'act_rem': actuall_remaining - running_done_total,
                'est_rem': total_estimate - estimate_sum
            }
            response_data.append(date_dict)
            total_estimate -= estimate_sum 

        return Response(response_data)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actuall_remaining = total_estimate

        serializer = self.get_serializer(queryset, many=True)
        data = defaultdict(list)

        for item in serializer.data:
            data[item['date']].append(item['data'][0])

        response_data = []
        running_done_total = 0

        for date, items in data.items():
            done_sum = 0
            estimate_sum = 0
            processed_items = []
            for item in items:
                out_of_estimate = item['estimate'] - item['done']
                item['out_of_estimate'] = out_of_estimate
                done_sum += item['done']
                estimate_sum += item['estimate']
                processed_items.append(item)  
            running_done_total += done_sum
            date_dict = {
                'date': date,
                'act_rem': actuall_remaining - running_done_total,
                'est_rem': total_estimate - estimate_sum
            }
            response_data.append(date_dict)
            total_estimate -= estimate_sum 

        return Response(response_data)



## chatbot
class CardCSVViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardChatbotSerializer  
    
    @staticmethod
    def closest_colour(hex_color):
        requested_colour = webcolors.hex_to_rgb(hex_color)
        min_colours = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]
    @staticmethod
    def get_colour_name(requested_colour):
        try:
            closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
        except ValueError:
            closest_name = closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name
    
    def export_csv(self):
        number = self.kwargs.get('pk')
        file_path=f'./media/csv/{number}.csv'
        lists = List.objects.filter(board=number)
        queryset = Card.objects.filter(list__in = lists)
        serializer = CardChatbotSerializer(queryset, many=True)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            keys = [
                        'title of card',
                        'list of the card',
                        'members of card',
                        'labels of card',
                        'start date of card',
                        'due date of card',
                        'reminder of card',
                        'storypoint of card',
                        'estimate of card',
                        'description of card',
                        'status of card'
                        ]
            writer.writerow(keys)

            for row in serializer.data:
                members_value = ', '.join([member.get('user', {}).get('username', '') for member in row.get('members', [])])
                labels_value = [
                        {'title': label.get('title', ''), 'color': self.closest_colour(label.get('color', ''))}
                        for label in row.get('labels', [])
                    ]                
                    
                writer.writerow([
                    row.get('title', ''),
                    row.get('list', {}).get('title', ''),
                    members_value,
                    labels_value,
                    row.get('startdate', ''),
                    row.get('duedate', ''),
                    row.get('reminder', ''),
                    row.get('storypoint', ''),
                    row.get('setestimate', ''),
                    row.get('description', ''),
                    row.get('status', ''),
                ])

    def get_queryset(self):
        self.export_csv()
        member_id = Member.objects.get(user_id = self.request.user.id)
        return Card.objects.filter(members = member_id)

class ChatbotAPIView(ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotRequestSerializer
    # @staticmethod
    def get_answer(self, number, request_message):
        agent = create_csv_agent(
        ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY),
        f"./media/csv/{number}.csv",
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,)

        return agent.run(request_message)

    def post(self, request, *args, **kwargs):
        serializer = ChatbotRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_message = serializer.validated_data.get('request_message')

        answer = self.get_answer(self.kwargs.get('pk'), request_message).replace("dataframe" , 'board')
        response_data = {"ai_message": answer}

        return Response(response_data)
    
    def get_queryset(self):
        return Chatbot.objects.none()


class BoardFilter(FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    has_star = BooleanFilter()
    lastseen = DateTimeFilter()

    class Meta:
        model = Board
        fields = ['title', 'has_star', 'lastseen']

class BoardfilterView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BoardFilter
    filterset_fields = ['title', 'has_star', 'lastseen']
    ordering_fields = ['title', 'has_star', 'lastseen']