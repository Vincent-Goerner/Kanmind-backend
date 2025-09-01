from rest_framework import serializers
from KanMind_App.models import User, Member, Board, Task, Column, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user', 'joined_date']

class BoardSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField(read_only=True)
    ticket_count = serializers.SerializerMethodField(read_only=True)
    tasks_to_do_count = serializers.SerializerMethodField(read_only=True)
    tasks_high_prio_count = serializers.SerializerMethodField(read_only=True)

    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        many=True,
        write_only=True,
        source='members'
    )
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count', 'tasks_high_prio_count', 'owner', 'members', 'member_ids', 'owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    
    def get_ticket_count(self, obj):
        return obj.tasks.count()
    
    def get_tasks_to_do_count(self, obj):
        return obj.columns.filter(type='TODO').count()
    
    def get_tasks_high_prio_count(self, obj):
        tasks = obj.tasks.filter(priority=Task.PriorityChoices.high)
        return tasks.count()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'board', 'description', 'status', 'priority']

class ColumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['title', 'assigned_tasks']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'task', 'owner', 'text', 'created']