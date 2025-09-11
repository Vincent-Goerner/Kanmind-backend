from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from kanmind.models import Board, Task, Comment
from kanmind.api.serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer, TaskDetailSerializer, CommentSerializer
from kanmind.api.permissions import IsOwnerOrMember, IsBoardMember, IsCommentAuthor
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from user_auth_app.api.serializers import UserProfileSerializer

class BoardListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsOwnerOrMember]

class EmailCheckView(generics.RetrieveAPIView):
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
        
class TaskListView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    permission_classes = [IsBoardMember]

class TaskListAssignedView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee_id=user)
    
class TaskListReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(reviewer_id=user)
    
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def perform_create(self, serializer: CommentSerializer):
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)
        
    def get_queryset(self):
        return Comment.objects.filter(task__id=self.kwargs.get("pk"))
    
class CommentDeleteView(generics.DestroyAPIView):
    # queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]

    def get_object(self):
        task_id = int(self.kwargs.get('pk'))
        comment_id = int(self.kwargs.get('comment_id'))
        return Comment.objects.get(pk=comment_id, task__id=task_id)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)