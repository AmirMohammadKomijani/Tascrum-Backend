from rest_framework import serializers
from .models import *
from Auth.serializers import UserProfileSerializer, UserTimelineSerializer
from Auth.models import User
from django.utils import timezone
import datetime
### Profile feature
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

### Home-Account inforamtion feature
class MemberWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id','name']

class MemberBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','title']

class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    workspaces = serializers.SerializerMethodField()
    boards = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id', 'profimage', 'user', 'workspaces','boards']
        
    def get_workspaces(self, obj):
        workspaces = obj.wmembers.all()
        return MemberWorkspaceSerializer(workspaces, many=True).data
    
    def get_boards(self, obj):
        boards = obj.bmembers.all()
        return MemberBoardSerializer(boards, many=True).data


### Workspace feature -> it includes all details about a workspace
class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','profimage','user']

class WorkspaceBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','title','backgroundImage','has_star']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['backgroundImage'] = "https://amirmohammadkomijani.pythonanywhere.com" + representation['backgroundImage']
        return representation


class WorkspaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberWorkspaceRole
        fields = ['id','role']

class WorkspaceSerializer(serializers.ModelSerializer):
    boards = serializers.SerializerMethodField()
    class Meta:
        model = Workspace
        fields = ['id','name','type','description','boards','backgroundImage']
   
    def get_boards(self, obj):
        roles = obj.wboard.all()
        return WorkspaceBoardSerializer(roles, many=True).data
    

class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id','name','type','description','backgroundImage']

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        workspace = Workspace.objects.create(**validated_data)
        MemberWorkspaceRole.objects.create(member=member, workspace=workspace, role="Owner")
        return workspace
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.backgroundImage = validated_data.get('backgroundImage', instance.backgroundImage)
        instance.save()
        return instance

### Board feature -> it includes all details about a board
class BoardMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','user']
class BoardMembersSerializer(serializers.ModelSerializer):
    members = BoardMemberSerializer(many=True)
    class Meta:
        model = Board
        fields = ['id','members']

    def get_members(self, obj):
        members = obj.members.order_by('id')
        return BoardMemberSerializer(members, many=True).data

    members = serializers.SerializerMethodField('get_members')

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id','title']

class BoardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','role']

class BoardSerializer(serializers.ModelSerializer):
    list = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','backgroundImage','workspace','list','lastseen','has_star']

    def get_list(self, obj):
        list = obj.lboard.all()
        return BoardListSerializer(list, many=True).data

class BoardInviteLink(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','invitation_link']
    

class CreateBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','title','workspace','backgroundImage','invitation_link']


    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        board = Board.objects.create(**validated_data)
        MemberBoardRole.objects.create(member=member, board=board, role="Owner")
        return board
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.backgroundImage = validated_data.get('backgroundImage' , instance.backgroundImage)
        instance.save()
        return instance


class BoardBackgroundImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','backgroundImage']

class BoardRecentlyViewed(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'backgroundImage','has_star']
class BoardStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','title','backgroundImage','has_star']

    # def update(self, instance, validated_data):
    #     instance.has_star = validated_data.get('has_star', instance.has_star)
    #     instance.save()
    #     return instance

class CreateBoardStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','has_star']

    def update(self, instance, validated_data):
        instance.has_star = validated_data.get('has_star', instance.has_star)
        instance.save()
        return instance

### List serializers
class ListBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id']

class ListCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','title','order']

class ListSerializer(serializers.ModelSerializer):
    card = serializers.SerializerMethodField()
    class Meta:
        model = List
        fields = ['id','title','board','card']
    
    def get_card(self, obj):
        cards = obj.clist.all()
        return ListCardSerializer(cards, many=True).data

class CreateListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id','title','board']
    
    def create(self, validated_data):
        return List.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.backgroundImage = validated_data.get('backgroundImage' , instance.backgroundImage)
        instance.save()
        return instance


###### Card Serializer
class CardMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','user']
class CardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id','title']
class CardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCardRole
        fields = ['id','role']

class CardLableSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Lable
        fields = '__all__'

## showing cards details
class CardSerializer(serializers.ModelSerializer):
    members = CardMemberSerializer(many=True)
    labels = CardLableSerialzier(many=True)
    role = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id','order','title','list','members','role','labels','startdate','duedate','reminder', 'storypoint', 'setestimate','description','status']

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data

## create card
class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id','title','list','startdate','duedate', 'reminder', 'storypoint', 'setestimate','description','status']

    def create(self, validated_data):
        # owner = Member.objects.get(user_id = self.context['user_id'])
        # board_role = MemberBoardRole.objects.filter(member = owner).first()

        # if board_role.role == "owner":
        validated_data['duedate'] = timezone.now()    
        card = Card.objects.create(**validated_data)
        MemberCardRole.objects.create(card)
        return card
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.startdate = validated_data.get('startdate' , instance.startdate)
        instance.duedate = validated_data.get('duedate' , instance.duedate)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.storypoint = validated_data.get('storypoint', instance.storypoint)
        instance.setestimate = validated_data.get('setestimate', instance.setestimate)
        instance.description = validated_data.get('description', instance.description)
        
        if instance.duedate < timezone.now():
            instance.status = validated_data.get('status', instance.status)
            instance.status = "overdue"
        instance.save()
        return instance


## Checklist in card
class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'content', 'checked', 'checklist']
    
    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        item = Item.objects.create(**validated_data)        
        return item

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.checked = validated_data.get('checked', instance.checked)
        instance.save()
        return instance

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'content', 'checked']

class ChecklistSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model = Checklist
        fields = ['id', 'title', 'items']
    
    def get_items(self, obj):
        items = obj.ichecklist.all()
        return ItemSerializer(items, many=True).data

class CardChecklistsSerializer(serializers.ModelSerializer):
    checklists = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ['id','checklists']
    
    def get_checklists(self,obj):
        checklist = obj.chcard.all()
        return ChecklistSerializer(checklist,many=True).data

class CreateChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = ['id', 'title', 'card']
    
    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        checklist = Checklist.objects.create(**validated_data)        
        return checklist

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

## Lables in Board
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lable
        fields = ['id', 'title', 'color']
class CreateLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lable
        fields = ['id', 'title', 'color', 'board']

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        label = Lable.objects.create(**validated_data)        
        return label

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.color = validated_data.get('color', instance.color)
        instance.save()
        return instance

class LabelBoardSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'labels']

    def get_labels(self, obj):
        label = obj.boardl.all()
        return LabelSerializer(label, many=True).data

# assign Labels to cards
class LabelCardAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardLabel
        fields = ['id', 'card', 'label']

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        label_card = CardLabel.objects.create(**validated_data)        
        return label_card

class lcSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardLabel
        fields = ['id']

class LabelCardSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    labelcard = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ["id", 'labels', 'labelcard']

    def get_labelcard(self, obj):
        lc = obj.cardl.all().order_by('label__id')
        return lcSerializer(lc, many=True).data
    
## assign members to card
class CardMemberAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id']
class CardAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberCardRole
        fields = ['id','card','member']
    
    def create(self, validated_data):
        # owner = Member.objects.get(user_id = self.context['user_id'])
        # board_role = MemberBoardRole.objects.filter(member = owner).first()
        return MemberCardRole.objects.create(**validated_data)
        # else:
        #     raise serializers.ValidationError("you are not owner of this board.")



#### invite member to board
class MemberFindUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['profimage']
class FindUserSerializer(serializers.ModelSerializer):
    member = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','member']
    
    def get_member(self,obj):
        members = obj.users.all()
        return MemberFindUserSerializer(members, many=True).data

class AddMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBoardRole
        fields = ['member','board']
    
    def create(self, validated_data):
        owner = Member.objects.get(user_id = self.context['user_id'])
        board = validated_data.get('board')
        newMember = validated_data.get('member')
        board_role = MemberBoardRole.objects.filter(member = owner,board=board).first()
        if board_role.role == "owner":
            if not MemberBoardRole.objects.filter(member = newMember,board=board).exists(): 
                return MemberBoardRole.objects.create(member = newMember,board=board,role='member')
            else:
                raise serializers.ValidationError("this member is part of this board already.")
        else:
            raise serializers.ValidationError("you are not owner of this board.")



### Drag and Drop

class Internal_DnDSerializer(serializers.ModelSerializer):
    class Meta:
        model=Card
        fields = ['id','list','order']


    def update(self, instance, validated_data):
        new_order = validated_data.get('order', instance.order)
        new_list = validated_data.get('list', instance.list)

        if instance.list == new_list:
            # Update order for cards in the same list
            if new_order < instance.order:
                cards = Card.objects.filter(list=instance.list, order__gte=new_order, order__lte=instance.order).exclude(
                    id=instance.id
                )
                for card in cards:
                    card.order += 1
                    card.save()
            elif new_order > instance.order:
                cards = Card.objects.filter(list=instance.list, order__gte=instance.order, order__lte=new_order).exclude(
                    id=instance.id
                )
                for card in cards:
                    card.order -= 1
                    card.save()

        elif instance.list != new_list:
            # Update order for cards in the old list with order greater than instance.order
            if new_order < instance.order:
                cards_to_update_old_list = Card.objects.filter(list=instance.list, order__gt=instance.order).exclude(
                    id=instance.id
                )
                            # Update order for cards in both cases
                for card in cards_to_update_old_list:
                    card.order -= 1
                    card.save()
            # Update order for cards in the new list with order greater than or equal to new_order
            elif new_order > instance.order:
                cards_to_update_new_list = Card.objects.filter(list=new_list, order__gte=new_order)
                for card in cards_to_update_new_list:
                    card.order += 1
                    card.save()

        instance.order = new_order
        instance.list = new_list
        instance.save()

        return instance



## timeline
#list
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
        card_members = MemberCardRole.objects.filter(member_id=member_id)
        card_ids = [card_member.card.id for card_member in card_members]
        cards = Card.objects.filter(id__in=card_ids)
        return CardsTimelineSerializer(cards, many=True).data

class MembersTimelineSerializer(serializers.ModelSerializer):
    members = MemberTimelineSerializer(many=True)
    class Meta:
        model = Board
        fields = ['id','members']




## burndown
class CreateBurndownChartSerializer(serializers.ModelSerializer):
    member_username = serializers.SerializerMethodField()
    class Meta:
        model = BurndownChart
        fields = ['id', 'member', 'date', 'done', 'estimate','board','member_username']

    def get_member_username(self, obj):
        return obj.member.user.username
    
    def create(self, validated_data):
        return BurndownChart.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'id': representation['id'],
            'date': representation['date'],
            'data': [
                {
                    'member': representation['member'],
                    'username': representation['member_username'],
                    'done': representation['done'],
                    'estimate': representation['estimate'],
                    'board': representation['board']
                }
            ]
        }
    
    def update(self, instance, validated_data):
        instance.done = validated_data.get('done', instance.done)
        instance.estimate = validated_data.get('estimate', instance.estimate)
        instance.save()
        return instance


#label
class LabelTimelineSerializer(serializers.ModelSerializer):
    cards = serializers.SerializerMethodField()
    class Meta:
        model = Lable
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



### Calender

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

## Review
class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self, survey):
        return serializers.serialize('json', survey.questions.all())

