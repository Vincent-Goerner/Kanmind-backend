from django.contrib import admin
from taskboard.models import Board, Task, Comment, Member

admin.site.register(Member)
admin.site.register(Board)
admin.site.register(Task)
admin.site.register(Comment)