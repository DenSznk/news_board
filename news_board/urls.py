from django.urls import path

from news_board.views import PostsListView, PostDetail, Approved, CommentsListView

urlpatterns = [
   path('', PostsListView.as_view(), name='posts'),
   path('<int:category_id>/', PostsListView.as_view(), name='categories'),
   path('post/<int:pk>', PostDetail.as_view(), name='post'),
   path('approved/<int:pk>/', CommentsListView.as_view(), name='approved'),
]
