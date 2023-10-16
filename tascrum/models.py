from django.db import models
from Auth.models import User


class Member(models.Model):

    occupations_choice = (
    ('Student','Student'),
    ('Employee','Employee'),
    ('Project Manager','Project Manager'),
    ('Other','Other'),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,related_name='users',null=False)\
    
    occupations = models.CharField(max_length=255,null=False,choices=occupations_choice)
    bio = models.TextField(null=True)
    profimage = models.ImageField(upload_to='Member/Profile',null=True,default='default_profile.png')
    birthdate = models.DateField(null=True)



class Workspace(models.Model):
    workspace_choice = (
    ('operations','operations'),
    ('education','education'),
    ('human resources','human resources'),
    ('small business','small business'),
    ('sales crm','sales crm'),
    ('engineering','engineering'),
    ('marketing','marketing'),
    ('Other','Other'),
    )
    
    name = models.CharField(max_length=255,null=True)
    type = models.CharField(max_length=20,choices=workspace_choice)
    description = models.TextField(null=True)
    members = models.ManyToManyField(Member, through='MemberWorkspaceRole', related_name='wmembers')


class MemberWorkspaceRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='mrole')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,related_name='wrole')
    role = models.CharField(max_length=50)


class Board(models.Model):
    title = models.CharField(max_length=255,null=False)
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name='wboard')
    members = models.ManyToManyField(Member, through='MemberBoardRole',related_name='bmembers')


class MemberBoardRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='bmember')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='brole')
    role = models.CharField(max_length=50)

class List(models.Model):
    title = models.CharField(max_length=255,null=False)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name='lboard')


class Card(models.Model):
    title = models.CharField(max_length=255,null=False)
    list = models.ForeignKey(List,on_delete=models.CASCADE,related_name='clist')
    members = models.ManyToManyField(Member, through='MemberCardRole',related_name='cmembers')

class MemberCardRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='cmember')
    card = models.ForeignKey(Card, on_delete=models.CASCADE,related_name='crole')
    role = models.CharField(max_length=50)