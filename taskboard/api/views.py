from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from taskboard.models import Board, Task, Comment
from taskboard.api.serializers import BoardSerializer, BoardDetailSerializer, TaskSerializer, CommentSerializer
from taskboard.api.permissions import IsOwnerOrMember, IsBoardMember, IsCommentAuthor
from django.shortcuts import get_object_or_404


class BoardListView(generics.ListCreateAPIView):
    """
    API view to list and create boards accessible to the authenticated user.
    Lists boards where the user is owner or member and validates members on creation.
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Returns boards where the user is either the owner or a member, without duplicates
        """
        user = self.request.user        
        boards = Board.objects.filter(members=user) | Board.objects.filter(owner=user)

        return boards.distinct()
    
    def get(self, request, *args, **kwargs):
        """
        Returns a serialized list of all boards the user has access to.
        """
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        Validates members input and delegates to the parent create method.
        Returns a 400 error if members is not a list of valid user IDs.
        """
        member_ids = request.data.get('members', [])

        if not isinstance(member_ids, list):
            return Response({"error": "Members must be a list of user IDs."}, status=status.HTTP_400_BAD_REQUEST)

        for member_id in member_ids:
            if not isinstance(member_id, int) and not str(member_id).isdigit():
                return Response({"error": "User dont exist"}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a board with detailed info.
    Access restricted to board owners or members.
    """
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsOwnerOrMember]
    
    def get(self, request, *args, **kwargs):
        """
        Retrieves and returns detailed information for a single board instance.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class TaskListView(generics.ListCreateAPIView):
    """
    API view to list and create tasks accessible to board members.
    Restricts access to users who are owners or members of the related board.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a task within a board.
    Access restricted to board owners and members.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsBoardMember]

    def delete(self, request, *args, **kwargs):
        """
        Deletes the specified task using the default destroy behavior.
        """
        return self.destroy(request, *args, **kwargs)

class TaskListAssignedView(generics.ListAPIView):
    """
    API view to list tasks assigned to the authenticated user.
    """ 
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns tasks where the current user is the assignee.
        """
        user = self.request.user
        return Task.objects.filter(assignee_id=user)
    
class TaskListReviewingView(generics.ListAPIView):
    """
    API view to list tasks assigned to the authenticated user as reviewer.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns tasks where the current user is the reviewer.
        """
        user = self.request.user
        return Task.objects.filter(reviewer_id=user)
    
class CommentCreateView(generics.ListCreateAPIView):
    """
    API view to list and create comments on a specific task.
    Ensures comments are linked to the task and authored by the current user.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def perform_create(self, serializer: CommentSerializer):
        """
        Saves a new comment linked to the specified task and sets the current user as author.
        """
        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, pk=task_id)
        serializer.save(author=self.request.user, task=task)
        
    def get_queryset(self):
        """
        Returns all comments associated with the specified task.
        """
        return Comment.objects.filter(task__id=self.kwargs.get("pk"))
    
class CommentDeleteView(generics.DestroyAPIView):
    """
    API view to delete a comment authored by the requesting user.
    Retrieves the comment by its ID and associated task ID before deletion.
    """
    queryset = Task.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]

    def get_object(self):
        """
        Retrieves a comment by ID that belongs to a specific task; used for deletion.
        """
        task_id = int(self.kwargs.get('pk'))
        comment_id = int(self.kwargs.get('comment_id'))
        return Comment.objects.get(pk=comment_id, task__id=task_id)