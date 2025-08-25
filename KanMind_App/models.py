from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)

class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(Member, related_name="boards")
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Column(models.Model):
    name = models.CharField(max_length=50)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='columns')

class Task(models.Model):
    PRIOITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    status = models.ForeignKey(Column, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIOITY_CHOICES, default='low')
    assignee_id = models.ManyToManyField(Member, related_name="tasks")
    reviewer_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_tasks")
    due_date = models.DateField(editable=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)