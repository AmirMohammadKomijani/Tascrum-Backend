from django.shortcuts import render
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MemberSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Member

# Create your views here.

class MemberProfileView(ModelViewSet):
    # queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # (member,created) = Member.objects.get_or_create(user_id = self.request.user.id)
        return Member.objects.filter(user_id = self.request.user.id)



