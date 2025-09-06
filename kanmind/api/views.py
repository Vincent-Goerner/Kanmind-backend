from rest_framework import generics
from kanmind.models import Board
from kanmind.api.serializers import BoardSerializer
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer