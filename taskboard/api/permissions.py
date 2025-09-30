from rest_framework.permissions import BasePermission, SAFE_METHODS
from taskboard.models import Board, Task, Comment
from rest_framework.exceptions import NotFound

class IsOwnerOrMember(BasePermission):
    """
    Permission class that grants access to board owners and members.
    Safe methods are allowed for all; only the owner can delete the board.
    Raises 404 if the board does not exist.
    """
    def has_permission(self, request, view):
        """
        Checks if the user is the board owner or a member; safe methods are always allowed.
        Raises a 404 error if the board does not exist.
        """
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
        """
        Allows access if the user is the board owner or a member; only the owner can delete the board.
        """
        board = obj

        if request.method == 'DELETE':
            return bool(request.user == board.owner)
        else:
            return bool(request.user == board.owner or request.user in board.members.all())
        
class IsBoardMember(BasePermission):
    """
    Permission class that allows access to board owners and members via board or task relation.
    Only the board owner or task creator can delete; raises 404 if board or task is missing.
    """
    def has_permission(self, request, view):
        """
        Checks if the user is a member or owner of the board linked via request data or task.
        Raises 404 if the board or task is not found.
        """
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
        """
        Allows access if user is board owner or member; only owner or task creator may delete.
        """
        task = obj
        try:
            board = task.board
        except:
            return False
        
        if request.method == "DELETE":
            return bool(request.user == board.owner or request.user == task.creator)
        
        return bool(request.user == board.owner or request.user in board.members.all())
    
class IsCommentAuthor(BasePermission):
    """
    Permission class that allows access only to the author of a comment.
    Raises 404 if the comment does not exist; only authors may delete their comments.
    """
    def has_permission(self, request, view):
        """
        Allows access only if the user is the author of the specified comment.
        Raises 404 if the comment does not exist.
        """
        try:
            comment = Comment.objects.get(pk=view.kwargs.get('comment_id'))
        except Comment.DoesNotExist:
            raise NotFound("Comment not found")
        if comment:
            return bool(request.user == comment.author)
    
    def has_object_permission(self, request, view, obj):
        """
        Allows deletion only if the user is the author of the comment.
        """
        comment = Comment.objects.get(pk=view.kwargs.get('comment_id'))
        if request.method == "DELETE":
            return bool(request.user == comment.author)