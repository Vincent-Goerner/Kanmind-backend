from rest_framework import serializers
from taskboard.models import Board, Task, Comment
from django.contrib.auth.models import User
from user_auth_app.api.serializers import UserProfileSerializer
from rest_framework.request import Request


def get_full_username(user):
    return f'{user.username} {user.last_name}'.strip()

class MembersField(serializers.Field):
    
    def to_representation(self, value:User):
        return UserProfileSerializer(value.all(), many=True).data
    
    def to_internal_value(self, data):
        users=[]
        for pk in data:
            try:
                user = User.objects.get(pk=pk)
                users.append(user)
            except User.DoesNotExist:
                raise serializers.ValidationError("User dont exist")
        return users

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    members = MembersField()
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id',
        ]

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()
    
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()
    
    def create(self, validated_data):
        members = validated_data.pop("members", [])
        request = self.context.get("request")
        owner = request.user

        board = Board.objects.create(owner=owner, **validated_data)

        board.members.set(members)
        return board
    
class TaskSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    assignee = UserProfileSerializer(read_only=True)
    reviewer = UserProfileSerializer(read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='assignee', 
        write_only=True,
        required=False,
        allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='reviewer', 
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer', 'assignee_id', 'reviewer_id', 'due_date', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        request = self.context.get("request")
        creator = request.user
        task = Task.objects.create(creator=creator, **validated_data)

        return task
    
class BoardDetailSerializer(BoardSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'members', 'tasks']
        write_only_fields = ['members']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request: Request = self.context.get("request")
        if request and request.method == "PATCH":
            rep["owner_data"] = UserProfileSerializer(instance.owner).data
            rep["members_data"] = UserProfileSerializer(instance.members.all(), many=True).data
            rep.pop("members", None)
        else:
            rep["owner_id"] = instance.owner_id
            rep["members"] = UserProfileSerializer(instance.members.all(), many=True).data
        return rep
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']
        
    def get_author(self, obj):
        return get_full_username(obj.author)