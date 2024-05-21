from rest_framework import generics, permissions
from rest_framework import filters
from blog.posts.api.v1.serializers import (
    PostSerializer,
    PostCommentSerializer,
    PostReactionSerializer,
)
from blog.posts.models import Post
from rest_framework.response import Response
from blog.posts.models import PostComment, PostReaction
from blog.posts.api.v1.permissions import(
    IsPostOwner,
    IsPostCommentOwner,
    IsReactionOwner
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model

User = get_user_model()


class CreatePostAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UpdatePostAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwner]
    
    def get_object(self):
        post_obj = Post.objects.filter(id=self.kwargs['id']).first()
        return post_obj
    
    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object()) # Checks if a user owns a post to be retrieved
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object()) # Checks if a user owns a post to be retrieved
        return super().put(request, *args, **kwargs)
    
class DeletePostAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsPostOwner]
    
    def get_object(self):
        post_obj = Post.objects.filter(id=self.kwargs['id']).first()
        return post_obj
    
    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object()) # Checks if a user owns a post to be retrieved        
        return super().delete(request, *args, **kwargs)

class UserPostsAPIView(generics.ListAPIView):
    """
        View for user to retrieve all there drafts or published posts
        # NOTE: default pagination set in REST_FRAMEWORK_SETTINGS
    """
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['post_state', 'title', 'content', 'category']

    def get_queryset(self):
        user_posts = Post.objects.filter(
            author=self.request.user
            ).select_related('author')
        return user_posts
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PublishedPostAPIView(generics.ListAPIView):
    """
        View for user to retrieve all published posts or a user
    """

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'category']
    
    def get_queryset(self):
        user = User.objects.filter(username=self.kwargs['username']).first()     
        user_posts = Post.objects.filter(
             author=user,
             post_state='published'
             )
        
        return user_posts
    
    @method_decorator(cache_page(60 * 5), name='post_five_mins_cache')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class AllPostAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['author__username', 'title', 'content', 'category']

    def get_queryset(self):
        post_objects = Post.objects.filter(post_state='published')
        return post_objects
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class PostCommentAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCommentSerializer

    def get_queryset(self):
        post = Post.objects.filter(id=self.kwargs["post_id"]).first()
        comments_to_post_objs = PostComment.objects.filter(
            post=post, parent_comment=None
        ).order_by('created_at')
        return comments_to_post_objs

    @method_decorator(cache_page(60 * 5), name='users_posts_five_mins_cache')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = {
            'post_id': self.kwargs['post_id']
            }
        self.get_serializer(context=context)
        return super().post(request, *args, **kwargs)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['post_id'] = self.kwargs['post_id']
        return context
    
class EditCommentAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostCommentOwner]

    def get_object(self):
        post_obj = PostComment.objects.filter(id=self.kwargs['comment_id']).first()
        return post_obj

    def get(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object())
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object())
        return super().put(request, *args, **kwargs)
    

class PostReactionAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostReactionSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DeleteReactionAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsReactionOwner]
    
    def get_object(self):
        reaction_obj = PostReaction.objects.filter(id=self.kwargs['reaction_id']).first()
        return reaction_obj
    
    def delete(self, request, *args, **kwargs):
        self.check_object_permissions(request, obj=self.get_object())
        return super().delete(request, *args, **kwargs)