from rest_framework import serializers
from .models import Member
from Auth.serializers import UserSerializer, UserProfileSerializer

class MemberSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    class Meta:
        model = Member
        fields = ['id', 'occupations', 'bio' ,'profimage', 'birthdate' ,  "user"]