from rest_framework import serializers
from .models import Member,Workspace,MemberWorkspaceRole,Board,MemberBoardRole,List,Card,MemberCardRole,Checklist,Item,Lable
from Auth.serializers import UserProfileSerializer
from Auth.models import User
from django.utils import timezone
from django.db.models import F

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
    # members = WorkspaceMemberSerializer(many=True)
    boards = serializers.SerializerMethodField()
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Workspace
        fields = ['id','name','type','description','boards','backgroundImage']

    def get_role(self, obj):
        roles = obj.wrole.all()
        return WorkspaceRoleSerializer(roles, many=True).data
    
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
        # workspace.members.add(member)

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

class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id','title']


class BoardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id','role']

class BoardSerializer(serializers.ModelSerializer):
    # members = BoardMemberSerializer(many=True)
    # role = serializers.SerializerMethodField()
    list = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','backgroundImage','workspace','list','lastseen','has_star']

    # def get_role(self, obj):
    #     roles = obj.brole.all()
    #     return BoardRoleSerializer(roles, many=True).data
    def get_list(self, obj):
        list = obj.lboard.all()
        return BoardListSerializer(list, many=True).data
    

class CreateBoardSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','workspace','backgroundImage']

    def get_role(self, obj):
        roles = obj.brole.all()
        return BoardRoleSerializer(roles, many=True).data

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        board = Board.objects.create(**validated_data)
        MemberBoardRole.objects.create(member=member, board=board, role="Owner")
        # Board.members.add(member)

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
        fields = ['id','title']

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

## showing cards details
class CardSerializer(serializers.ModelSerializer):
    members = CardMemberSerializer(many=True)
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id','title','list','members','startdate','duedate','reminder', 'storypoint', 'setestimate']

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data

## create card
class CreateCardSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id','title','list','startdate','duedate', 'reminder', 'storypoint', 'setestimate']

    def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        validated_data['duedate'] = timezone.now()
        card = Card.objects.create(**validated_data)
        MemberCardRole.objects.create(member=member, card=card, role="assigned")

        return card
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.startdate = validated_data.get('startdate' , instance.startdate)
        instance.duedate = validated_data.get('duedate' , instance.duedate)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.storypoint = validated_data.get('storypoint', instance.storypoint)
        instance.setestimate = validated_data.get('setestimate', instance.setestimate)
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
        instance.title = validated_data.get('content', instance.content)
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

## Lables in card
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

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lable
        fields = ['id', 'title', 'color', 'board']

class LabelBoardSerializer(serializers.ModelSerializer):
    labels = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id', 'labels']

    def get_labels(self,obj):
        label = obj.blable.all()
        return LabelSerializer(label,many=True).data
    
## assign members to card
class CardMemberAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id']
class CardAssignSerializer(serializers.ModelSerializer):
    # members = CardMemberAssignSerializer(many=True)
    # board = serializers.IntegerField()
    class Meta:
        model = MemberCardRole
        fields = ['id','card','member']
    
    def create(self, validated_data):
        owner = Member.objects.get(user_id = self.context['user_id'])
        # board_id = validated_data.get('board')
        board_role = MemberBoardRole.objects.filter(member = owner).first()
        if board_role.role == "owner":
            # members_data = validated_data.pop('member')
            # for member_data in members_data:
            #     member_id = member_data['id']
            #     member = Member.objects.get(id=member_id)
            return MemberCardRole.objects.create(**validated_data)
        else:
            raise serializers.ValidationError("you are not owner of this board.")



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
        instance.list = validated_data.get('list', instance.list)
        if new_order < instance.order:
            cards = Card.objects.filter(list=instance.list,order__gte = new_order,order__lte=instance.order).exclude(id = instance.id)
            for card in cards:
                card.order += 1
                card.save()
        elif new_order > instance.order:
            cards = Card.objects.filter(list=instance.list,order__gte=instance.order,order__lte=new_order).exclude(id = instance.id)
            for card in cards:
                card.order -= 1
                card.save()
        instance.order = new_order
        instance.save()
        return instance


    # def update(self, instance, validated_data):
    #     new_order = validated_data.get('order', instance.order)
    #     current_order = instance.order
    #     target_list = instance.list

    #     # Update the order of the current instance
    #     instance.order = new_order

    #     # Update the order of cards after changing the order of the current instance
    #     if new_order < current_order:
    #         # Move cards down in order
    #         Card.objects.filter(list=target_list, order__gt=new_order, order__lte=current_order).exclude(id=instance.id).update(order=F('order') + 1)
    #     elif new_order > current_order:
    #         # Move cards up in order
    #         Card.objects.filter(list=target_list, order__lt=new_order, order__gte=current_order).exclude(id=instance.id).update(order=F('order') - 1)
    #     instance.save()

    #     return instance

