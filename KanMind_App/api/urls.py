from django.urls import path
from KanMind_App.api.views import BoardList

urlpatterns = [
    path('boards/', BoardList.as_view(), name='board-list'),
    # path('manufacturers/', ManufacturerList.as_view(), name='manufacturer-list'),
]