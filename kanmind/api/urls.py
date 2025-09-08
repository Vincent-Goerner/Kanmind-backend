from django.urls import path
from kanmind.api.views import BoardList, BoardDetail

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetail.as_view(), name='board-detail')
]