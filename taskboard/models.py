from django.db import models
from django.contrib.auth.models import User
from datetime import date


STATUS_SELECTION=(
    ('to-do','To Do'),
    ('in-progress','In Progress'),
    ('review','Review'),
    ('done','Done')
)

PRIORITY_SELECTION=(
    ('low','Low'),
    ('medium','Medium'),
    ('high','High')
)

class Member(models.Model):
    """
    Represents a registered user who is a member of the system.
    Links one-to-one with Django's User model and stores the join date.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Board(models.Model):
    """
    Represents a project board that can have multiple members and tasks.
    Each board has one owner and can be shared with other users as members.
    """
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name="board_members")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    """
    Represents a task within a board, including its status, priority, and assignments.
    Tasks can have assignees, reviewers, due dates, and are linked to a creator.
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_SELECTION, default='to-do')
    priority = models.CharField(max_length=10, choices=PRIORITY_SELECTION, default='medium')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_assignees")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_reviewer")
    due_date = models.DateField(editable=True, default=date.today())
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='task_creator')

    def __str__(self):
        return self.title

class Comment(models.Model):
    """
    Represents a comment made on a specific task by a user.
    Stores content, creation timestamp, and links to both task and author.
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text