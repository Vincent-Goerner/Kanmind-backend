from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from taskboard.models import Board, Task, Comment
from taskboard.api.serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer, CommentSerializer
from taskboard.api.permissions import IsOwnerOrMember, IsBoardMember, IsCommentAuthor
from django.shortcuts import get_object_or_404


class BoardListView(generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user        
        boards = Board.objects.filter(members=user) | Board.objects.filter(owner=user)

        return boards.distinct()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        member_ids = request.data.get('members', [])

        if not isinstance(member_ids, list):
            return Response({"error": "Members must be a list of user IDs."}, status=status.HTTP_400_BAD_REQUEST)

        for member_id in member_ids:
            if not isinstance(member_id, int) and not str(member_id).isdigit():
                return Response({"error": "User dont exist"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsOwnerOrMember]
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

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
    
class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def perform_create(self, serializer: CommentSerializer):
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)
        
    def get_queryset(self):
        return Comment.objects.filter(task__id=self.kwargs.get("pk"))
    
class CommentDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]

    def get_object(self):
        task_id = int(self.kwargs.get('pk'))
        comment_id = int(self.kwargs.get('comment_id'))
        return Comment.objects.get(pk=comment_id, task__id=task_id)