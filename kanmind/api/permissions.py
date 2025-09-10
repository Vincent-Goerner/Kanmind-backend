from rest_framework.permissions import BasePermission,IsAuthenticated , SAFE_METHODS
from kanmind.models import Board, Task
from rest_framework.exceptions import NotFound

class IsOwnerOrMember(IsAuthenticated):

    def has_permission(self, request, view):
        user = request.user
        method = request.method

        try:
            board = Board.objects.get(pk=view.kwargs.get('pk'))
        except Board.DoesNotExist:
            raise NotFound("Board does not exist")
        if method in SAFE_METHODS:
            return True
        return bool(user == board.owner or user in board.members.all())
    
    def has_object_permission(self, request, view, obj):
        board = obj

        if request.method == 'DELETE':
            return bool(request.user == board.owner)
        else:
            return bool(request.user == board.owner or request.user in board.members.all())
        
class IsBoardMember(BasePermission):

    def has_permission(self, request, view):
        board_id = request.data.get("board")
        if board_id:
            try:
                board = Board.objects.get(pk=board_id)
            except Board.DoesNotExist:
                raise NotFound("Board does not exist")
        else:
            try:
                task = Task.objects.get(pk=view.kwargs.get("pk"))
                board = task.board
            except:
                raise NotFound("Task does not exist")
        return (
            request.user == board.owner or
            board.members.filter(id=request.user.id).exists()
        )
    
    def has_object_permission(self, request, view, obj):
        task = obj
        try:
            board = task.board
        except:
            return False
        
        if request.method == "DELETE":
            return bool(request.user == board.owner or request.user == task.owner)
        
        return bool(request.user == board.owner or request.user in board.members.all())