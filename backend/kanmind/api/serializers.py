from rest_framework import serializers
from kanmind.models import Board, Task, Comment
from django.contrib.auth.models import User
from user_auth_app.api.serializers import UserProfileSerializer


def get_full_username(user):
    return f'{user.username} {user.last_name}'.strip()

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    members = UserProfileSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'members', 'member_ids', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to_do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    
    def create(self, validated_data):
        members = validated_data.pop("members", [])
        request = self.context.get("request")
        owner = request.user if request else None

        board = Board.objects.create(owner=owner, **validated_data)

        board.members.set(members)
        return board
    
class BoardDetailSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_id', 'members', 'member_ids', 'tasks']

class TaskSerializer(serializers.ModelSerializer):
    creator_id = serializers.PrimaryKeyRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'comments_count', 'creator_id']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        request = self.context.get("request")
        creator = request.user
        task = Task.objects.create(creator=creator, **validated_data)

        return task
    
class TaskDetailSerializer(TaskSerializer):
    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee_id', 'reviewer_id', 'due_date', 'creator_id']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        
    def get_author(self, obj):
        return get_full_username(obj.author)