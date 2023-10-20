from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    username = models.CharField(default='user',null=True,max_length=20,unique=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','password']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'
    )
