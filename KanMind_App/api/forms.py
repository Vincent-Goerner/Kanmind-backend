from django.forms import ModelForm
from KanMind_App.models import Board

# Beispiel:

# class ArticleForm(ModelForm):
#     class Meta:
#         model = Article
#         fields = ["pub_date", "headline", "content", "reporter"]

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ["title", "members"]