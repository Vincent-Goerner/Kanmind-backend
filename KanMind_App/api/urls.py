from django.urls import path
from KanMind_App.apis.views import BoardList

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
]