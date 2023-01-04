from django import forms
from django.conf import settings
from django.core.mail import send_mail

from news_board.models import Post, Comment, Category
from users.models import User


class PostForm(forms.ModelForm):
    header = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Title'
    }))
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Description'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)
    video = forms.URLField(widget=forms.TextInput(
        attrs={'class': 'form-control py-4',
               'placeholder': 'video'}))
    category = forms.ModelChoiceField(
        label='Category', queryset=Category.objects.all(), widget=forms.Select(
            attrs={'class': 'form-control py-4'},
        )
    )

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
        print('formhello')
        comment = super(CommentForm, self).save(commit=True)
        record = Comment.objects.create(comment=comment)
        record.send_email_for_new_comment()
