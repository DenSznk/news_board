from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from news_board.forms import CommentForm, PostForm
from news_board.models import Category, Post, Comment
from users.models import User


class IndexView(TemplateView):
    template_name = 'news_board/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['title'] = 'Home'
        return context


class PostsListView(ListView):
    """list of posts sorted by category"""
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


class PostDetail(DetailView):
    model = Post
    template_name = 'news_board/post.html'
    context_object_name = 'news'
    form_class = CommentForm

    def get_context_data(self, **kwargs, ):
        data = super(PostDetail, self).get_context_data(**kwargs)

        comments = Comment.objects.filter(post=self.get_object()).order_by('-added')
        paginator = Paginator(comments, 10)
        page = self.request.GET.get('page')
        data['comments_page'] = paginator.get_page(page)
        data['comments'] = comments
        data['title'] = 'News Board Post'

        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(body=request.POST.get('body'),
                              user=self.request.user,
                              post=self.get_object())
        new_comment.save()
        posts_user = Post.objects.get(id=kwargs['pk']).user
        send_mail(
            subject='New Comment',
            message=f'You have new comment',
            from_email=settings.EMAIL_FROM,
            recipient_list=[posts_user.email]
        )
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'news_board/add_post.html'
    form_class = PostForm
    title = 'Add post'

    def get_context_data(self, **kwargs):
        data = super(AddPost, self).get_context_data(**kwargs)
        data['title'] = 'Add Post'
        return data

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_board/delete_post.html'
    success_url = reverse_lazy('posts')


class PostUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news_board/add_post.html'


class CommentApproved(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'news_board/comment_approved.html'
    form_class = CommentForm
    context_object_name = 'approved'
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comment_id = self.kwargs.get('pk')
        Comment.objects.filter(pk=comment_id).update(approved=True)
        data['message'] = 'Comment was approved'
        user = self.object.user
        send_mail(
            subject='Approved comment',
            message=f'user approved your comment.',
            from_email=settings.EMAIL_FROM,
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
        )
        return data


class CommentDisapproved(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'news_board/comment_disapproved.html'
    success_url = reverse_lazy('posts')


class CommentsFilterView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'news_board/comments_filter.html'
    paginate_by = 10
    ordering = 'id'

    def get_queryset(self):
        queryset = super(CommentsFilterView, self).get_queryset()
        post_id = self.kwargs.get('post_id')
        return queryset.filter(post_id=post_id) if post_id else queryset.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super(CommentsFilterView, self).get_context_data()
        data['post_comments'] = Post.objects.filter(user=self.request.user)

        return data
