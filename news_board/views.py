from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormMixin, UpdateView

from news_board.forms import CommentForm
from news_board.models import Category, Post, Comment
from users.models import User


class IndexView(TemplateView):
    template_name = 'news_board/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Home'
        return context


class PostsListView(ListView):
    model = Post
    template_name = 'news_board/posts.html'
    paginate_by = 3
    ordering = 'id'

    def get_queryset(self):
        queryset = super(PostsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostsListView, self).get_context_data()
        context['title'] = 'News Board'
        context['categories'] = Category.objects.all()
        return context


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'news_board/post.html'
    context_object_name = 'news'
    form_class = CommentForm
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        comments_connected = Comment.objects.filter(
            post=self.get_object()).order_by('-added')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        comment = Comment(body=request.POST.get('body'),
                          user=self.request.user,
                          post=self.get_object())

        comment.save()
        return self.get(self, request, *args, **kwargs)


class Approved(UpdateView):
    model = Comment
    template_name = 'news_board/approved.html'
    form_class = CommentForm
    context_object_name = 'approved'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы приняли отклик!'
        comment_id = self.kwargs.get('pk')
        Comment.objects.filter(pk=comment_id).update(approved=True)
        user = self.object.user
        send_mail(
            subject='Ваш отклик опубликован!',
            message=f'Пользователь опубликовал Ваш отклик.',
            from_email=settings.EMAIL_FROM,
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
        )
        return context


class Cans(UpdateView):
    model = Comment
    template_name = 'accept.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Вы отменили отклик!'
        comment_id = self.kwargs.get('pk')
        Comment.objects.filter(pk=comment_id).delelete()
        return context


class CommentsListView(ListView):
    template_name = 'news_board/comments.html'
    model = Comment
    context_object_name = 'comments'
    ordering = '-added'

    def get_queryset(self):
        queryset = super(CommentsListView, self).get_queryset()
        post_id = self.kwargs.get('post_id')
        return queryset.filter(post_id=post_id) if post_id else queryset



