from django.urls import path
from blog.posts.api.v1.views import (
    CreatePostAPIView,
    UpdatePostAPIView,
    DeletePostAPIView,
    UserPostsAPIView,
    PostAPIView,
    PostCommentAPIView,
    EditCommentAPIView,
    PostReactionAPIView,
    DeleteReactionAPIView,
    AllPostAPIView
)

urlpatterns = [
    path('create-post/',CreatePostAPIView.as_view(), name='create_post'),
    path('update-post/<uuid:id>/', UpdatePostAPIView.as_view(), name='updta_post'),
    path('delete-post/<uuid:id>/', DeletePostAPIView.as_view(), name='delete_post'),
    path('user-posts/', UserPostsAPIView.as_view(), name='user-posts'),
    path('all-posts/', AllPostAPIView.as_view(), name='all_posts'),
    path('posts/<str:username>/', PostAPIView.as_view(), name='posts'),
    path('post-comment/<uuid:post_id>/', PostCommentAPIView.as_view(), name='post_comment' ),
    path('edit-comment/<uuid:comment_id>/', EditCommentAPIView.as_view(), name='edit_comment'),
    path('post-reaction/', PostReactionAPIView.as_view(), name='post_reaction'),
    path('delete-reaction/<uuid:reaction_id>/', DeleteReactionAPIView.as_view(), name='delete_reaction')
]