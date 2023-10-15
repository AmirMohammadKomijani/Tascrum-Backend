from rest_framework import serializers
from .models import Member,Workspace
from Auth.serializers import UserProfileSerializer



class MemberWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id','name']

class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    workspaces = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = ['id', 'occupations', 'bio', 'profimage', 'birthdate', 'user', 'workspaces']
        
    def get_workspaces(self, obj):
        workspaces = obj.wmembers.all()
        return MemberWorkspaceSerializer(workspaces, many=True).data



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