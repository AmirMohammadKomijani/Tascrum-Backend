from rest_framework import serializers
from .models import Member,Workspace,MemberWorkspace
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

class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    workspaces = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id', 'profimage', 'user', 'workspaces']
        
    def get_workspaces(self, obj):
        workspaces = obj.wmembers.all()
        return MemberWorkspaceSerializer(workspaces, many=True).data


### Workspace feature -> it includes all details about a workspace
class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','profimage','user']

class WorkspaceSerializer(serializers.ModelSerializer):
    members = WorkspaceMemberSerializer(many=True)
    class Meta:
        model = Workspace
        fields = ['id','name','type','description','members']
    
    def create(self, validated_data):
        # Get the member ID from the serializer data
        member_id = Member.objects.get(user_id = self.context['user_id'])
        validated_data['member'] = member_id

        # Create a new Workspace instance with role="Owner"
        workspace = Workspace.objects.create(**validated_data)

        # Get the Member instance based on the provided member ID
        member = Member.objects.get(id=member_id)

        # Create a MemberWorkspace instance to associate the member with the workspace and role="Owner"
        MemberWorkspace.objects.create(member=member, workspace=workspace, role="Owner")

        return workspace


class CreateWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id','name','type','description']

    def create(self, validated_data):
        member = Member.objects.get(user_id = self.context['user_id'])
        workspace = Workspace.objects.create(**validated_data)
        MemberWorkspace.objects.create(member=member, workspace=workspace, role="Owner")
        # workspace.members.add(member)

        return workspace






### Board feature -> it includes all details about a board