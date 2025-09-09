from django.urls import path
from kanmind.api.views import BoardList, BoardDetail, EmailCheck, TaskList

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetail.as_view(), name='board-detail'),
    path('email-check/', EmailCheck.as_view(), name='email-check'),
    path('tasks/', TaskList.as_view(), name='tasks-list'),
]