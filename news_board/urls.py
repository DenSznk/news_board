from django.urls import path

from news_board.views import (PostsListView, PostDetail,
                              AddPost, PostDelete, PostUpdate, CommentApproved,
                              CommentDisapproved, CommentsFilterView)

urlpatterns = [
    path('', PostsListView.as_view(), name='posts'),
    path('comments', CommentsFilterView.as_view(), name='comments_filter'),
    path('comments/<int:post_id>/', CommentsFilterView.as_view(), name='comment_post'),
    path('<int:category_id>/', PostsListView.as_view(), name='categories'),
    path('add-post/', AddPost.as_view(), name='add_post'),
    path('delete-post/<int:pk>/', PostDelete.as_view(), name='delete_post'),
    path('update-post/<int:pk>/', PostUpdate.as_view(), name='update_post'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('approved/<int:pk>/', CommentApproved.as_view(), name='comment_approved'),
    path('disapproved/<int:pk>/', CommentDisapproved.as_view(), name='comment_disapproved'),
]
