from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)

class Board(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="boards")

class Task(models.Model):
    board = models.ManyToManyField(Board,related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=30)
    priority = models.CharField(max_length=30)
    assignee_id = models.ManyToManyField(User, related_name="tasks")
    reviewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(editable=True)