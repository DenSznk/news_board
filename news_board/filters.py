from django_filters import FilterSet
from .models import Comment, Post


class CommentFilter(FilterSet):
    class Meta:
        model = Post

        fields = {
            'user': ['exact'],
        }
