from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    header = models.CharField(max_length=100)
    video = EmbedVideoField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='image/%Y/%m/%d')
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_set',
        verbose_name='author,'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_set',
    )

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post=self).count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user_set')
    body = models.CharField(max_length=255)
    added = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.body} to {self.user}'
