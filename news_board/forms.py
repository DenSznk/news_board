from django import forms

from news_board.models import Post, Comment


class PostForm(forms.ModelForm):
    video = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Enter video link',

        }), required=False)

    class Meta:
        model = Post
        fields = ('header', 'content', 'image', 'video', 'category')


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Comment'

    }))

    class Meta:
        model = Comment
        fields = ('body',)
