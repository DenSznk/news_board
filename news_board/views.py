from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView

from news_board.forms import CommentForm, PostForm
from news_board.models import Category, Post, Comment


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


class PostDetail(DetailView):
    model = Post
    template_name = 'news_board/post.html'
    context_object_name = 'news'
    form_class = CommentForm
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        data = super(PostDetail, self).get_context_data(**kwargs)

        comments = Comment.objects.filter(
            post=self.get_object()).order_by('-added')
        data['comments'] = comments
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            new_comment = Comment(body=request.POST.get('body'),
                                  user=self.request.user,
                                  post=self.get_object())
            new_comment.save()
            return self.get(self, request, *args, **kwargs)
        else:
            return reverse_lazy('posts')


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'news_board/add_post.html'
    form_class = PostForm
    success_url = reverse_lazy('posts')
    success_message = 'Post added'
    title = 'Add post'

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
    success_url = reverse_lazy('posts')
