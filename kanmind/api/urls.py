from django.urls import path
from kanmind.api.views import BoardListView, BoardDetailView, EmailCheckView, TaskListView, TaskListAssignedView, TaskListReviewingView, TaskDetailView, CommentCreateView, CommentDeleteView

urlpatterns = [
    path('boards/', BoardListView.as_view(), name='board-list'),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
    path('tasks/', TaskListView.as_view(), name='tasks-list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='tasks-detail'),
    path('tasks/assigned-to-me/', TaskListAssignedView.as_view(), name='tasks-assignee'),
    path('tasks/reviewing/', TaskListReviewingView.as_view(), name='tasks-review'),
    path('tasks/<int:pk>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('tasks/<int:pk>/comments/<int:comment_id>/', CommentDeleteView.as_view(), name='comment-delete'),
]