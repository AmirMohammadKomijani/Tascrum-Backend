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
    backgroundImage = models.ImageField(upload_to='images/',default='default_profile.png')


class MemberWorkspaceRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='mrole')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE,related_name='wrole')
    role = models.CharField(max_length=50)


class Board(models.Model):
    title = models.CharField(max_length=255,null=False)
    workspace = models.ForeignKey(Workspace,on_delete=models.CASCADE,related_name='wboard')
    members = models.ManyToManyField(Member, through='MemberBoardRole',related_name='bmembers')
    backgroundImage = models.ImageField(null=True, upload_to='images/')

class MemberBoardRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='bmember')
    board = models.ForeignKey(Board, on_delete=models.CASCADE,related_name='brole')
    role = models.CharField(max_length=50,default='member')

class List(models.Model):
    title = models.CharField(max_length=255,null=False)
    board = models.ForeignKey(Board,on_delete=models.CASCADE,related_name='lboard')


class Card(models.Model):
    title = models.CharField(max_length=255,null=False)
    list = models.ForeignKey(List,on_delete=models.CASCADE,related_name='clist')
    members = models.ManyToManyField(Member, through='MemberCardRole',related_name='cmembers')
    startdate = models.DateTimeField(null=True)
    duedate = models.DateTimeField(null=True)
    storypoint = models.IntegerField(default=0)
    setestimate = models.IntegerField(default=0)
    reminder_choice =(
    ('At time of due date','At time of due date'),
    ('1 Day before','1 Day before'),
    ('2 Day before','2 Day before'),
    ('3 Day before','3 Day before'),
    ('5 Days before','5 Days before'),
    ('None','None'),
    ) 
    reminder = models.CharField(max_length=30,choices=reminder_choice , default='1 Day before')

class Checklist(models.Model):
    title = models.CharField(max_length=60, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='chcard')

class Item(models.Model):
    content = models.CharField(max_length=255, null=True)
    checked = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='ichecklist')

class Lable(models.Model):
    color = models.CharField(max_length=30, null=False)
    title = models.CharField(max_length=30, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='blable')

class MemberCardRole(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE,related_name='cmember')
    card = models.ForeignKey(Card, on_delete=models.CASCADE,related_name='crole')
    role = models.CharField(max_length=50,default='member')


class BurndownChart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='burndown_charts')
    date = models.DateField(null=False)
    done = models.IntegerField(default=0)
    estimate = models.IntegerField(default=0)

