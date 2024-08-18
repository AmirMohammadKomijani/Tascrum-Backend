from rest_framework import serializers
from .models import *
from Auth.serializers import UserProfileSerializer, UserTimelineSerializer
from Auth.models import User
from django.utils import timezone

class MemberProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id', 'occupations', 'bio', 'profimage', 'birthdate', 'user']

    def update(self, instance, validated_data):
        instance.occupations = validated_data.get('occupations',instance.occupations)
        instance.bio = validated_data.get('bio',instance.bio)
        instance.profimage = validated_data.get('profimage',instance.profimage)
        instance.birthdate = validated_data.get('birthdate',instance.birthdate)
        instance.save()
        
        user_data = validated_data.pop('user', None)
        user = instance.user
        user_serializer = UserProfileSerializer(user, data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return instance

class ChangePasswordSerializer(serializers.ModelSerializer):
    Newpassword = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['Newpassword']

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['Newpassword'])
        user.save()
        return user
class MemberWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name']


class MemberBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title']


class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    workspaces = serializers.SerializerMethodField()
    boards = serializers.SerializerMethodField()

    class Meta:
        model = Member
        fields = ['id', 'profimage', 'user', 'workspaces', 'boards']

    def get_workspaces(self, obj):
        workspaces = obj.wmembers.all()
        return MemberWorkspaceSerializer(workspaces, many=True).data

    def get_boards(self, obj):
        boards = obj.bmembers.all()
        return MemberBoardSerializer(boards, many=True).data


class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Member
        fields = ['id', 'profimage', 'user']


class WorkspaceMembersSerializer(serializers.ModelSerializer):
    members = WorkspaceMemberSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ['id', 'members']


class WorkspaceBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'backgroundimage', 'has_star']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['backgroundimage'] = (
            "https://amirmohammadkomijani.pythonanywhere.com" + representation['backgroundimage']
        )
        return representation


class WorkspaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberWorkspaceRole
        fields = ['id', 'role']


class WorkspaceSerializer(serializers.ModelSerializer):
    boards = serializers.SerializerMethodField()

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'type', 'description', 'boards', 'backgroundimage']

    def get_boards(self, obj):
        roles = obj.wboard.all()
        return WorkspaceBoardSerializer(roles, many=True).data


class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name', 'type', 'description', 'backgroundimage']

    def create(self, validated_data):
        member = Member.objects.get(user_id=self.context['user_id'])
        workspace = Workspace.objects.create(**validated_data)
        MemberWorkspaceRole.objects.create(member=member, workspace=workspace, role="Owner")
        return workspace

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.backgroundimage = validated_data.get('backgroundimage', instance.backgroundimage)
        instance.save()
        return instance


class BoardMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Member
        fields = ['id', 'user']


class BoardMembersSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'members']

    def get_members(self, obj):
        members = obj.members.order_by('id')
        return BoardMemberSerializer(members, many=True).data


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title']


class BoardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'role']


class BoardSerializer(serializers.ModelSerializer):
    list = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'backgroundimage', 'workspace', 'list',
            'lastseen', 'has_star', 'invitation_link'
        ]

    def get_list(self, obj):
        board_list = obj.lboard.all()
        return BoardListSerializer(board_list, many=True).data


class BoardProfileSerializer(serializers.ModelSerializer):
    workspace = WorkspaceSerializer(read_only=True)
    list = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'backgroundimage', 'workspace', 'list',
            'lastseen', 'has_star', 'invitation_link'
        ]

    def get_list(self, obj):
        board_list = obj.lboard.all()
        return BoardListSerializer(board_list, many=True).data


class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'workspace', 'backgroundimage', 'invitation_link']

    def create(self, validated_data):
        member = Member.objects.get(user_id=self.context['user_id'])
        board = Board.objects.create(**validated_data)
        MemberBoardRole.objects.create(member=member, board=board, role="Owner")
        return board

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.backgroundimage = validated_data.get('backgroundimage', instance.backgroundimage)
        instance.save()
        return instance


class BoardBackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'backgroundimage']


class BoardRecentlyViewed(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'backgroundimage', 'has_star']


class BoardStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'backgroundimage', 'has_star']


class CreateBoardStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'has_star']

    def update(self, instance, validated_data):
        instance.has_star = validated_data.get('has_star', instance.has_star)
        instance.save()
        return instance


class ListBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id']


class ListCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'order']


class ListSerializer(serializers.ModelSerializer):
    card = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ['id', 'title', 'board', 'card']

    def get_card(self, obj):
        cards = obj.clist.all()
        return ListCardSerializer(cards, many=True).data


class ListProfileSerializer(serializers.ModelSerializer):
    board = BoardProfileSerializer(read_only=True)
    card = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ['id', 'title', 'board', 'card']

    def get_card(self, obj):
        cards = obj.clist.all()
        return ListCardSerializer(cards, many=True).data


class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title', 'board']

    def create(self, validated_data):
        return List.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.backgroundimage = validated_data.get(
            'backgroundimage', instance.backgroundimage
        )
        instance.save()
        return instance


class CardMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = Member
        fields = ['id', 'user']


class CardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title']


class CardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCardRole
        fields = ['id', 'role']


class CardLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    members = CardMemberSerializer(many=True)
    labels = CardLabelSerializer(many=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            'id', 'order', 'title', 'list', 'members', 'role', 'labels',
            'startdate', 'duedate', 'reminder', 'storypoint', 'setestimate',
            'description', 'status', 'comment'
        ]

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data


class CardProfileSerializer(serializers.ModelSerializer):
    members = CardMemberSerializer(many=True)
    labels = CardLabelSerializer(many=True)
    list = ListProfileSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = [
            'id', 'order', 'title', 'list', 'members', 'role', 'labels',
            'startdate', 'duedate', 'reminder', 'storypoint', 'setestimate',
            'description', 'status', 'comment'
        ]

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data


class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id', 'title', 'list', 'startdate', 'duedate', 'reminder',
            'storypoint', 'setestimate', 'description', 'status', 'comment'
        ]

    def create(self, validated_data):
        validated_data['duedate'] = validated_data['startdate'] + timezone.timedelta(days=7)
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.startdate = validated_data.get('startdate', instance.startdate)
        instance.duedate = validated_data.get('duedate', instance.duedate)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.storypoint = validated_data.get('storypoint', instance.storypoint)
        instance.setestimate = validated_data.get('setestimate', instance.setestimate)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class ChecklistCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id']


class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'name', 'is_completed']


class ChecklistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = Checklist
        fields = ['id', 'card', 'title', 'items']

    def get_items(self, obj):
        items = obj.citems.all()
        return ChecklistItemSerializer(items, many=True).data


class CreateChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ['id', 'card', 'title']

    def create(self, validated_data):
        return Checklist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.card = validated_data.get('card', instance.card)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance


class CreateChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['id', 'checklist', 'name', 'is_completed']

    def create(self, validated_data):
        return ChecklistItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance


class LabelBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id']


class LabelSerializer(serializers.ModelSerializer):
    board = LabelBoardSerializer(read_only=True)

    class Meta:
        model = Label
        fields = ['id', 'name', 'color', 'board']


class CreateLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'color', 'board']

    def create(self, validated_data):
        return Label.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance


class LabelCardAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'labels']

    def update(self, instance, validated_data):
        instance.labels.set(validated_data.get('labels'))
        instance.save()
        return instance


class CardAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'members']

    def update(self, instance, validated_data):
        instance.members.set(validated_data.get('members'))
        instance.save()
        return instance


class InviteMemberBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'members']

    def update(self, instance, validated_data):
        instance.members.add(validated_data['new_member'])
        instance.save()
        return instance


class DragDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'order']

    def update(self, instance, validated_data):
        instance.order = validated_data.get('order', instance.order)
        instance.save()
        return instance


class TimelineCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'duedate', 'status']


class TimelineListSerializer(serializers.ModelSerializer):
    cards = TimelineCardSerializer(many=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'cards']


class TimelineBoardSerializer(serializers.ModelSerializer):
    lists = TimelineListSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'lists']


class TimelineWorkspaceSerializer(serializers.ModelSerializer):
    boards = TimelineBoardSerializer(many=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'boards']

class CardsTimelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','title','startdate','duedate']
class ListBoardTimelineSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    class Meta:
        model = List
        fields = ['id','title','cards']
    
    def get_cards(self, obj):
        cards = obj.clist.all().order_by('startdate', 'duedate')
        return CardsTimelineSerializer(cards, many=True).data
class ListTimelineSerializer(serializers.ModelSerializer):
    lists = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'lists']

    def get_lists(self, obj):
        lists = obj.lboard.all()
        return ListBoardTimelineSerializer(lists, many=True).data

#member
class MemberTimelineSerializer(serializers.ModelSerializer):
    user = UserTimelineSerializer()
    cards = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id','user','profimage','cards']
        
    def get_cards(self, obj): 
        member_id = obj.id
        view = self.context.get('view')  
        board_id = view.kwargs.get('pk')
        # board_id = self.kwargs['pk'] 
        lists = List.objects.filter(board=board_id) 
        card_members = MemberCardRole.objects.filter(member_id=member_id) 
        card_ids = [card_member.card.id for card_member in card_members] 
        cards = Card.objects.filter(id__in=card_ids, list__in=lists) 
        return CardsTimelineSerializer(cards, many=True).data

class MembersTimelineSerializer(serializers.ModelSerializer):
    members = MemberTimelineSerializer(many=True)
    class Meta:
        model = Board
        fields = ['id','members']


class LabelTimelineSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    class Meta:
        model = Label
        fields = ['id', 'title', 'color', 'cards']

    def get_cards(self, obj):
        label_id = obj.id  
        card_labels = CardLabel.objects.filter(label_id=label_id)
        card_ids = [card_label.card.id for card_label in card_labels]
        cards = Card.objects.filter(id__in=card_ids)
        return CardsTimelineSerializer(cards, many=True).data
class LabelsTimelineSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'labels']

    def get_labels(self, obj):
        label = obj.boardl.all()
        return LabelTimelineSerializer(label, many=True).data

class TimelineStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['startdate']

class TimelineDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['duedate']


class BurndownCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'title', 'duedate']


class BurndownListSerializer(serializers.ModelSerializer):
    cards = BurndownCardSerializer(many=True)

    class Meta:
        model = List
        fields = ['id', 'title', 'cards']


class BurndownBoardSerializer(serializers.ModelSerializer):
    lists = BurndownListSerializer(many=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'lists']


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'time', 'title']

class CalenderSerializer(serializers.ModelSerializer):
    members = CardMemberSerializer(many=True)
    labels = CardLableSerialzier(many=True)
    role = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id','order','title','list','members','role','labels','startdate','duedate','reminder', 'storypoint', 'setestimate','description','status']

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data
