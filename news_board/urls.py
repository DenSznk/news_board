from django.urls import path

from news_board.views import PostsListView, PostDetail, CommentsListView, AddPost, PostDelete, PostUpdate

urlpatterns = [
   path('', PostsListView.as_view(), name='posts'),
   path('<int:category_id>/', PostsListView.as_view(), name='categories'),
   path('add-post/', AddPost.as_view(), name='add_post'),
   path('delete-post/<int:pk>/', PostDelete.as_view(), name='delete_post'),
   path('update-post/<int:pk>/', PostUpdate.as_view(), name='update_post'),
   path('post/<int:pk>', PostDetail.as_view(), name='post'),
   path('approved/<int:pk>/', CommentsListView.as_view(), name='approved'),
]
