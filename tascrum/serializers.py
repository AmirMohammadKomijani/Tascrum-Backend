from rest_framework import serializers
from .models import Member,Workspace,MemberWorkspaceRole,Board,MemberBoardRole
from Auth.serializers import UserProfileSerializer


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


class WorkspaceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberWorkspaceRole
        fields = ['id','role']

class WorkspaceSerializer(serializers.ModelSerializer):
    members = WorkspaceMemberSerializer(many=True)
    # role = serializers.SerializerMethodField()
    class Meta:
        model = Workspace
        fields = ['id','name','type','description','members']

    # def get_role(self, obj):
    #     roles = obj.wrole.all()
    #     return WorkspaceRoleSerializer(roles, many=True).data
    

class CreateWorkspaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workspace
        fields = ['id','name','type','description']


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
        instance.save()
        return instance
        



### Board feature -> it includes all details about a board
class BoardMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','user']


class BoardRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberBoardRole
        fields = ['id','role']

class BoardSerializer(serializers.ModelSerializer):
    members = BoardMemberSerializer(many=True)
    role = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','workspace','role','members']

    def get_role(self, obj):
        roles = obj.brole.all()
        return BoardRoleSerializer(roles, many=True).data
    

class CreateBoardSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = Board
        fields = ['id','title','workspace','role']

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
        instance.save()
        return instance