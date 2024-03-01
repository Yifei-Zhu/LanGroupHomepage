from django.db import models
from django.contrib.auth.models import User

class DutyGroup(models.Model):
    # name = models.CharField(max_length=100)
    num = models.IntegerField(unique=True)
    users = models.ManyToManyField(User, related_name='duty_groups')

    def __str__(self):
        return f'Group {str(self.num)}'

    def list_users(self):
        return ", ".join([f"{user.first_name} {user.last_name}" for user in self.users.all()])

