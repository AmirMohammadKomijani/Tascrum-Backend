from rest_framework import serializers
from .models import Member,Workspace,MemberWorkspaceRole,Board,MemberBoardRole,List,Card,MemberCardRole
from Auth.serializers import UserProfileSerializer
from Auth.models import User
from django.utils import timezone



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
        fields = ['id','title']


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
        model = MemberBoardRole
        fields = ['id','role']

class BoardSerializer(serializers.ModelSerializer):
    # members = BoardMemberSerializer(many=True)
    # role = serializers.SerializerMethodField()
    list = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','workspace','list','backgroundImage']

    def get_role(self, obj):
        roles = obj.brole.all()
        return BoardRoleSerializer(roles, many=True).data
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
        fields = ['id','title','list','members','startdate','duedate','reminder']


def get_role(self, obj):
        roles = obj.crole.all()
        return CardRoleSerializer(roles, many=True).data
    
## create card
class CreateCardSerializer(serializers.ModelSerializer):
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = ['id','title','list','startdate','duedate', 'reminder']

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
        instance.save()
        return instance

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

class FindUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

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
            return MemberBoardRole.objects.create(member = newMember,board=board,role='member')
        else:
            raise serializers.ValidationError("you are not owner of this board.")


