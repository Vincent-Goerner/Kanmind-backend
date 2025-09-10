from django.db import models
from django.contrib.auth.models import User
from datetime import date


STATUS_SELECTION=(
    ('todo','To Do'),
    ('in_progress','In Progress'),
    ('review','Review'),
    ('done','Done')
)

PRIORITY_SELECTION=(
    ('low','Low'),
    ('medium','Medium'),
    ('high','High')
)

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="board_members")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_SELECTION, default='to-do')
    priority = models.CharField(max_length=10, choices=PRIORITY_SELECTION, default='medium')
    assignee_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_assignees")
    reviewer_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_reviewer")
    due_date = models.DateField(editable=True, default=date.today())
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_creator')

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text