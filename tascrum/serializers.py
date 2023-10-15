from rest_framework import serializers
from .models import Member,Workspace
from Auth.serializers import UserProfileSerializer

class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id', 'occupations', 'bio' ,'profimage', 'birthdate' ,  "user"]





class WorkspaceMemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id','profimage','user']



class WorkspaceSerializer(serializers.ModelSerializer):
    members = WorkspaceMemberSerializer(many=True)
    class Meta:
        model = Workspace
        fields = ['name','type','description','members']