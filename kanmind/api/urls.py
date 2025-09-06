from django.urls import path
from kanmind.api.views import BoardList

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
]