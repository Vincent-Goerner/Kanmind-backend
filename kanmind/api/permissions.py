from rest_framework.permissions import BasePermission,IsAuthenticated , SAFE_METHODS
from kanmind.models import Board
from rest_framework.exceptions import NotFound

class IsOwnerOrMember(IsAuthenticated):

    def has_object_permission(self, request, view, obj):

        try:
            board = obj
        except Board.DoesNotExist:
            raise NotFound("Board does not exist")
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return bool(request.user == board.owner)
        else:
            return bool(request.user == board.owner or request.user in board.members.all())