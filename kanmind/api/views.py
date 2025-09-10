from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kanmind.models import Board, Task
from kanmind.api.serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer
from kanmind.api.permissions import IsOwnerOrMember
from django.contrib.auth.models import User
from user_auth_app.api.serializers import UserProfileSerializer

class BoardList(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

class BoardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsOwnerOrMember]

class EmailCheck(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        check_email = request.query_params.get('email')

        if not check_email:
            return Response({'error': 'no valid email'} ,status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=check_email)
            user_data = UserProfileSerializer(user).data
            return Response(user_data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class TaskList(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]