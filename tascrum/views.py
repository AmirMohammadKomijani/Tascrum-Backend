from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from Auth.models import User
from .models import (Member, Workspace, Board, Label, Card, Checklist, Item,
                     Meeting, CardLabel, MemberCardRole, MemberBoardRole)
from .serializers import *

class MemberProfileView(ModelViewSet):
    allowed_methods = ('GET', 'PUT', 'HEAD', 'OPTIONS')
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.filter(user_id=self.request.user.id)


class ChangePasswordView(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class WorkspaceView(ModelViewSet):
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Workspace.objects.filter(members=member_id)


class CreateWorkspaceView(ModelViewSet):
    serializer_class = CreateWorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Workspace.objects.filter(members=member_id)


class WorkspaceMembersView(ModelViewSet):
    serializer_class = WorkspaceMembersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Workspace.objects.filter(id=self.kwargs['workspace_pk'], members=member_id)


class BoardViewSet(ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Board.objects.filter(members=member_id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.lastseen = datetime.now()
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='join/(?P<invitation_link>[^/.]+)')
    def join(self, request, invitation_link=None):
        board = get_object_or_404(Board, invitation_link=invitation_link)
        member, created = Member.objects.get_or_create(user_id=request.user.id)

        if not board.members.filter(id=member.id).exists():
            board.members.add(member)
            return Response({'status': 'Member added to the board', 'board_id': board.id}, status=status.HTTP_200_OK)
        return Response({'status': 'Member already in board', 'board_id': board.id}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reset(self, request, pk=None):
        board = self.get_object()
        board.invitation_link = str(uuid.uuid4())
        board.save()

        return Response({'status': 'Invitation link reset', 'new_invitation_link': board.invitation_link}, status=status.HTTP_200_OK)


class BoardImageView(ModelViewSet):
    serializer_class = BoardBackgroundImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Board.objects.filter(members=member_id)


class CreateBoardView(ModelViewSet):
    serializer_class = CreateBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def perform_create(self, serializer):
        board = serializer.save()
        colors = ['#e67c73', '#f7cb4d', '#41b375', '#7baaf7', '#ba67c8']
        for color in colors:
            Lable.objects.create(board=board, color=color, title='')

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Board.objects.filter(members=member_id)


class BoardMembersView(ModelViewSet):
    serializer_class = BoardMembersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Board.objects.filter(members=member_id)


class BoardStarView(ModelViewSet):
    serializer_class = BoardStarSerializer

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
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


class BoardRecentlyViewedView(ModelViewSet):
    serializer_class = BoardRecentlyViewed
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Board.objects.filter(members=member_id).order_by('-lastseen')[:3]


class BoardInvitationLinkView(ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_invitation_link(self, request):
        board_id = request.GET.get('board_id')
        invitation_link = Board.objects.get(id=board_id).invitation_link
        return HttpResponse(invitation_link)


class ListView(ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        board_ids = Board.objects.filter(members=member_id).values_list('id', flat=True)
        return List.objects.filter(board__in=board_ids)


class CreateListView(ModelViewSet):
    serializer_class = CreateListSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        board_ids = Board.objects.filter(members=member_id).values_list('id', flat=True)
        return List.objects.filter(board__in=board_ids)


class CardView(ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.request.query_params.get('board')
        list_ids = List.objects.filter(board=board_id).values_list('id', flat=True)
        return Card.objects.filter(list__in=list_ids)


class CardViewMember(ModelViewSet):
    serializer_class = CardProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Card.objects.filter(members__user=user)
        label_ids = self.request.query_params.getlist('label_ids')
        if label_ids:
            queryset = queryset.filter(labels__id__in=label_ids).distinct()
        return queryset


class BoardCardsViewSet(ModelViewSet):
    serializer_class = CardProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        board_ids = Board.objects.filter(members__user=user).values_list('id', flat=True)
        list_ids = List.objects.filter(board__in=board_ids).values_list('id', flat=True)
        queryset = Card.objects.filter(list__in=list_ids)
        label_ids = self.request.query_params.getlist('label_ids')
        if label_ids:
            queryset = queryset.filter(labels__id__in=label_ids).distinct()
        return queryset


class UserBoardLabelsViewSet(ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        board_ids = Board.objects.filter(members__user=user).values_list('id', flat=True)
        return Lable.objects.filter(board__in=board_ids).distinct()


class CreateCardView(ModelViewSet):
    serializer_class = CreateCardSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Card.objects.filter(members=member_id)


class CardAssignmentView(ModelViewSet):
    queryset = MemberCardRole.objects.all()
    serializer_class = CardProfileSerializer


class Internal_DndView(ModelViewSet):
    serializer_class = Internal_DnDSerializer

    @action(detail=True, methods=['put'])
    def move_card(self, request, pk=None):
        card = self.get_object()
        serializer = self.get_serializer(card, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateChecklistView(ModelViewSet):
    serializer_class = CreateChecklistSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Checklist.objects.filter(members=member_id)


class ChecklistView(ModelViewSet):
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        return Checklist.objects.filter(card_id=self.kwargs['card_pk'])


class CardChecklistView(ModelViewSet):
    serializer_class = CardChecklistsSerializer

    def get_queryset(self):
        return Checklist.objects.filter(card_id=self.kwargs['card_pk'])


class CreateItemView(ModelViewSet):
    serializer_class = CreateItemSerializer

    def get_queryset(self):
        return Item.objects.filter(checklist_id=self.kwargs['checklist_pk'])


class LabelBoardView(ModelViewSet):
    serializer_class = LabelBoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        board_ids = Board.objects.filter(members=member_id).values_list('id', flat=True)
        return Lable.objects.filter(board__in=board_ids)


class LabelCardAssignView(ModelViewSet):
    serializer_class = LabelCardAssignSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Card.objects.filter(members=member_id)


class LabelCardView(ModelViewSet):
    serializer_class = LabelCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        board_ids = Board.objects.filter(members=member_id).values_list('id', flat=True)
        label_ids = Lable.objects.filter(board__in=board_ids).values_list('id', flat=True)
        return Card.objects.filter(labels__id__in=label_ids).distinct()


class FindUserView(ModelViewSet):
    serializer_class = FindUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)


class InviteMemberView(ModelViewSet):
    serializer_class = AddMemberSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class HomeAccountView(ModelViewSet):
    serializer_class = MemberProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Member.objects.filter(user_id=self.request.user.id)


class ListTimelineView(ModelViewSet):
    serializer_class = TimelineListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.request.query_params.get('board_id')
        return List.objects.filter(board_id=board_id).order_by('-created_at')


class MemberTimelineView(ModelViewSet):
    serializer_class = MembersTimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Card.objects.filter(members=member_id).order_by('-created_at')


class LabelTimelineView(ModelViewSet):
    serializer_class = LabelsTimelineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        label_id = self.request.query_params.get('label_id')
        return Card.objects.filter(labels__id=label_id).order_by('-created_at')


class TimelineStartPeriodView(ModelViewSet):
    serializer_class = TimelineStartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        return Card.objects.filter(start_date__gte=start_date)


class TimelineDuePeriodView(ModelViewSet):
    serializer_class = TimelineDueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        due_date = self.request.query_params.get('due_date')
        return Card.objects.filter(due_date__lte=due_date)


class CreateMeetingView(ModelViewSet):
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

    def get_queryset(self):
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Meeting.objects.filter(members=member_id)


class MeetingView(ModelViewSet):
    serializer_class = MeetingSerializer

    def get_queryset(self):
        return Meeting.objects.filter(board_id=self.kwargs['board_pk'])


class CalenderView(ModelViewSet):
    serializer_class = CalenderSerializer

    def get_queryset(self):
        return Card.objects.filter(board_id=self.kwargs['board_pk'])


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
            actual_name = webcolors.rgb_to_name(requested_colour)
            closest_name = actual_name
        except ValueError:
            closest_name = CardCSVView.closest_colour(requested_colour)
            actual_name = None
        return actual_name, closest_name

    def export_csv(self):
        number = self.kwargs.get('pk')
        file_path = f'./media/csv/{number}.csv'
        lists = List.objects.filter(board=number)
        queryset = Card.objects.filter(list__in=lists)
        serializer = CardChatbotSerializer(queryset, many=True)

        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            keys = [
                'title of card', 'list of the card', 'members of card',
                'labels of card', 'start date of card', 'due date of card',
                'reminder of card', 'storypoint of card', 'estimate of card',
                'description of card', 'status of card'
            ]
            writer.writerow(keys)

            for row in serializer.data:
                members_value = ', '.join(
                    [member.get('user', {}).get('username', '') for member in row.get('members', [])]
                )
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
        member_id = Member.objects.get(user_id=self.request.user.id)
        return Card.objects.filter(members=member_id)


class ChatbotAPIView(ModelViewSet):
    queryset = Chatbot.objects.all()
    serializer_class = ChatbotRequestSerializer

    def get_answer(self, number, request_message):
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY),
            f"./media/csv/{number}.csv",
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )
        return agent.run(request_message)

    def post(self, request, *args, **kwargs):
        serializer = ChatbotRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_message = serializer.validated_data.get('request_message')

        answer = self.get_answer(self.kwargs.get('pk'), request_message).replace("dataframe", 'board')
        response_data = {"ai_message": answer}

        return Response(response_data)

    def get_queryset(self):
        return Chatbot.objects.none()


class BurndownChartViewSet(ModelViewSet):
    serializer_class = CreateBurndownChartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board_id = self.kwargs.get('pk')
        user = self.request.user.id
        return BurndownChart.objects.filter(
            board_id=board_id, board__members=user
        ).order_by('date', 'member__id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actual_remaining = total_estimate

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
                'act_rem': actual_remaining - running_done_total,
                'est_rem': total_estimate - estimate_sum
            }
            response_data.append(date_dict)
            total_estimate -= estimate_sum

        return Response(response_data)

    def retrieve(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        total_estimate = queryset.aggregate(Sum('estimate'))['estimate__sum'] or 0
        actual_remaining = total_estimate

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
                'act_rem': actual_remaining - running_done_total,
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