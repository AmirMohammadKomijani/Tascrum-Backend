from django.db import models
from Auth.models import User
import uuid
from django.core.exceptions import ValidationError

# Choices
OCCUPATION_CHOICES = [
    ('Student', 'Student'),
    ('Employee', 'Employee'),
    ('Project Manager', 'Project Manager'),
    ('Other', 'Other'),
]

WORKSPACE_CHOICES = [
    ('operations', 'Operations'),
    ('education', 'Education'),
    ('human resources', 'Human Resources'),
    ('small business', 'Small Business'),
    ('sales crm', 'Sales CRM'),
    ('engineering', 'Engineering'),
    ('marketing', 'Marketing'),
    ('Other', 'Other'),
]

REMINDER_CHOICES = [
    ('At time of due date', 'At time of due date'),
    ('1 Day before', '1 Day before'),
    ('2 Days before', '2 Days before'),
    ('3 Days before', '3 Days before'),
    ('5 Days before', '5 Days before'),
    ('None', 'None'),
]

STATUS_CHOICES = [
    ('Done', 'Done'),
    ('overdue', 'Overdue'),
    ('pending', 'Pending'),
    ('failed', 'Failed'),
]


class Member(models.Model):
    """Represents a user within the system with profile details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members', null=False)
    occupation = models.CharField(max_length=255, choices=OCCUPATION_CHOICES, null=False)
    bio = models.TextField(null=True)
    profile_image = models.ImageField(upload_to='Member/Profile', null=True, default='default_profile.png')
    birthdate = models.DateField(null=True)


class Workspace(models.Model):
    """Represents a workspace where members collaborate."""
    name = models.CharField(max_length=255, null=True)
    type = models.CharField(max_length=20, choices=WORKSPACE_CHOICES)
    description = models.TextField(null=True)
    members = models.ManyToManyField(Member, through='MemberWorkspaceRole', related_name='workspaces')
    background_image = models.ImageField(upload_to='images/', default='default_profile.png')


class MemberWorkspaceRole(models.Model):
    """Defines roles of members in workspaces."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='workspace_roles')
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='member_roles')
    role = models.CharField(max_length=50)


class Board(models.Model):
    """Represents a board within a workspace for managing tasks."""
    title = models.CharField(max_length=255, null=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='boards')
    members = models.ManyToManyField(Member, through='MemberBoardRole', related_name='boards')
    has_star = models.BooleanField(default=False)
    invitation_link = models.CharField(max_length=255, default=uuid.uuid4, unique=True)
    background_image = models.ImageField(upload_to='images/', default='default_profile.png')
    last_seen = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.invitation_link:
            self.invitation_link = str(uuid.uuid4())
        super().save(*args, **kwargs)


class MemberBoardRole(models.Model):
    """Defines roles of members on boards."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='board_roles')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='member_roles')
    role = models.CharField(max_length=50, default='member')


class Meeting(models.Model):
    """Represents a scheduled meeting on a board."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='meetings')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='meetings')
    title = models.CharField(max_length=255, null=False, default='Meeting')
    time = models.DateTimeField(null=False)

    class Meta:
        ordering = ['time']


class List(models.Model):
    """Represents a list of tasks within a board."""
    title = models.CharField(max_length=255, null=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='lists')


class Label(models.Model):
    """Represents a label that can be attached to tasks within a board."""
    color = models.CharField(max_length=30, null=False)
    title = models.CharField(max_length=30, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='labels')


class Card(models.Model):
    """Represents a task card within a list."""
    title = models.CharField(max_length=255, null=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='cards')
    members = models.ManyToManyField(Member, through='MemberCardRole', related_name='cards')
    start_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    story_point = models.IntegerField(default=0)
    set_estimate = models.IntegerField(default=0)
    reminder = models.CharField(max_length=30, choices=REMINDER_CHOICES, default='1 Day before')
    order = models.IntegerField(null=True, auto_created=True)
    labels = models.ManyToManyField(Label, through='CardLabel', related_name='cards')
    comment = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError("Due date must be after start date.")
        
        if not self.order:
            max_order_in_list = Card.objects.filter(list=self.list).aggregate(models.Max('order'))['order__max']
            self.order = max_order_in_list + 1 if max_order_in_list is not None else 1
        
        super().save(*args, **kwargs)


class CardLabel(models.Model):
    """Defines the association between cards and labels."""
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='card_labels')
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name='label_cards')

    class Meta:
        unique_together = ('card', 'label')
        ordering = ['label']


class Checklist(models.Model):
    """Represents a checklist within a card."""
    title = models.CharField(max_length=60, null=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='checklists')


class Item(models.Model):
    """Represents an item within a checklist."""
    content = models.CharField(max_length=255, null=True)
    checked = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')


class MemberCardRole(models.Model):
    """Defines roles of members on cards."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='card_roles')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='member_roles')
    role = models.CharField(max_length=50, default='member')

    class Meta:
        ordering = ['member']


class BurndownChart(models.Model):
    """Represents a burndown chart for tracking progress on a board."""
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='burndown_charts')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='burndown_charts')
    date = models.DateField(null=False)
    done = models.FloatField(default=0)
    estimate = models.FloatField(default=0)


class Question(models.Model):
    """Represents a question in a survey."""
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=255)


class Survey(models.Model):
    """Represents a survey containing multiple questions."""
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question, through='SurveyQuestion', related_name='surveys')


class SurveyQuestion(models.Model):
    """Defines the association between surveys and questions."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Chatbot(models.Model):
    """Represents a chatbot interaction with a request message."""
    request_message = models.CharField(max_length=500)
