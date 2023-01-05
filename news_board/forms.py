from django import forms

from news_board.models import Post, Comment


class PostForm(forms.ModelForm):
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

    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=True)
        record = Comment.objects.create(comment=comment)
        record.send_email_for_new_comment()
