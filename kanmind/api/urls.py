from django.urls import path
from kanmind.api.views import BoardList, BoardDetail, EmailCheck, TaskList, TaskListAssigned, TaskListReviewing, TaskDetail

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetail.as_view(), name='board-detail'),
    path('email-check/', EmailCheck.as_view(), name='email-check'),
    path('tasks/', TaskList.as_view(), name='tasks-list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='tasks-detail'),
    path('tasks/assigned-to-me/', TaskListAssigned.as_view(), name='tasks-assignee'),
    path('tasks/reviewing/', TaskListReviewing.as_view(), name='tasks-review'),
]