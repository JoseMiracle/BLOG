from factory.django import DjangoModelFactory
from blog.posts.models import Post, PostComment, PostReaction, PostImage
from tests.accounts.factories import UserFactory
import factory

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = 'I like reading'
    author = factory.SubFactory(UserFactory)
    content = 'I love reading a lot'
    category = 'travel'
    post_state = 'published'


class PostCommentFactory(DjangoModelFactory):
    
    class Meta:
        model = PostComment
    
    post = factory.SubFactory(PostFactory)
    parent_comment = factory.SubFactory('tests.posts.factories.PostCommentFactory', parent_comment=None)
    user_that_comment = factory.SelfAttribute('post.author')
    comment = 'I love dogs too'

class PostImageFactory(DjangoModelFactory):
    class Meta:
        model = PostImage

    post = factory.SubFactory(PostFactory)
    image = factory.django.ImageField(filename='test_image.jpg')

class PostReactionFactory(DjangoModelFactory):

    class Meta:
        model = PostReaction
    

    post = factory.SubFactory(PostFactory)
    user_that_react = factory.SelfAttribute('post.author')
    reaction = 'upvote'
