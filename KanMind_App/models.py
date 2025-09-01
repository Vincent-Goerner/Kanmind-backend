from django.db import models
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class Board(models.Model):
    title = models.CharField(max_length=50)
    members = models.ManyToManyField(Member, related_name="boards")
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new_board = self._state.adding

        super().save(*args, **kwargs)

        if is_new_board:
            self.columns = [
                ('TODO', 'To Do'),
                ('IN_PROGRESS', 'In Progress'),
                ('REVIEW', 'Review'),
                ('DONE', 'Done'),
            ]
            for index, (column_type) in enumerate(columns):
                Column.objects.create(board=self, type=column_type, order=index)

    def __str__(self):
        return self.title
    
class Column(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=20,
        choices=[
            ('TODO', 'To Do'),
            ('IN_PROGRESS', 'In Progress'),
            ('REVIEW', 'Review'),
            ('DONE', 'Done'), 
        ])

    def __str__(self):
        return f"{self.get_type_display()} ({self.board.title})"

class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        low = 'Low'
        medium = 'Medium'
        high = 'High'

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    status = models.ForeignKey(Column, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PriorityChoices.choices, default='low')
    assignee_id = models.ManyToManyField(Member, related_name="tasks")
    reviewer_id = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name="reviewed_tasks")
    due_date = models.DateField(editable=True, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text