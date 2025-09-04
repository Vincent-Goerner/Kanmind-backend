from rest_framework import generics
from KanMind_App.models import Board
from KanMind_App.apis.serializers import BoardSerializer
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer