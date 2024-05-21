from rest_framework.test import APITestCase, APIRequestFactory
from blog.posts.models import Post, PostImage
from tests.posts.utils import generate_image_file, generate_invalid_file
from blog.posts.api.v1.serializers import(
    PostSerializer, 
    PostCommentSerializer, 
    PostReactionSerializer
) 
from tests.accounts.factories import UserFactory
from tests.posts.factories import PostFactory
from blog.posts.models import (
    PostComment, 
    PostImage, 
    CommentToPostImages,
    PostReaction
)


class TestPostSerializer(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(email='delight@mail.com')
        self.user.set_password('delightpassword')
        self.user.save()

    def test_post_can_be_created_with_valid_data(self):
        """Test post can be created with valid data"""
        request = self.factory.post('/')
        request.user = self.user

        valid_data = {
            'title': 'Love a dog',
            'post_state': 'published',
            'content': "My love for dog is undisputed",
            'category': 'lifestyle',
            'uploaded_images': [generate_image_file()]
        }

        serializer = PostSerializer(data=valid_data, context={'request': request})
        self.assertTrue(serializer.is_valid())

        serializer.save()
        
        number_of_post = Post.objects.count()
        self.assertEqual(number_of_post, 1)

    def test_post_cannot_be_created_with_invalid_data(self):
        """Test post cannot be created with invalid data"""
        
        valid_data = {
            'title': 'Love a dog',
            'content': "My love for dog is undisputed",
            'category': 'lifestyle',
            'uploaded_images': [generate_invalid_file()]
        }

        serializer = PostSerializer(data=valid_data)
        self.assertFalse(serializer.is_valid())
        
        number_of_post = Post.objects.count()
        self.assertEqual(number_of_post, 0)

    
    def test_multiple_images_can_be_uploaded_with_post(self):
        """Test multiple images can be uploaded with post"""
        request = self.factory.post('/')
        request.user = self.user

        valid_data = {
            'title': 'Love a dog',
            'post_state': 'published',
            'content': "My love for dog is undisputed",
            'category': 'lifestyle',
            'uploaded_images': [generate_image_file(), generate_image_file(), generate_image_file()]
        }

        serializer = PostSerializer(data=valid_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        
        serializer.save()
        
        post = Post.objects.filter(author=self.user).first()
        self.assertIsNotNone(post)
        
        post_images =  PostImage.objects.filter(post=post)
        self.assertEqual(post_images.count(), 3) 



class TestPostCommentSerializer(APITestCase):


    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.factory = APIRequestFactory()
        self.request = self.factory.post('/')
        self.request.user = self.user

    def test_create_comment_with_images(self):
        """Test creating a comment with images"""

        data = {
            'comment': 'This is a test comment',
            'uploaded_comment_to_post_images': [generate_image_file(), generate_image_file()]
        }

        serializer = PostCommentSerializer(data=data, context={'post_id': self.post.id, 'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()
        self.assertEqual(comment.comment, 'This is a test comment')
        self.assertEqual(comment.user_that_comment, self.user)
        self.assertEqual(comment.post, self.post)

        images = CommentToPostImages.objects.filter(comment_to_post=comment)
        self.assertEqual(images.count(), 2)

    def test_create_comment_without_images(self):
        """Test creating a comment without images"""

        data = {
            'comment': 'This is a test comment without images'
        }

        serializer = PostCommentSerializer(data=data, context={'post_id': self.post.id, 'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

        comment = serializer.save()
        self.assertEqual(comment.comment, 'This is a test comment without images')
        self.assertEqual(comment.user_that_comment, self.user)
        self.assertEqual(comment.post, self.post)

        images = CommentToPostImages.objects.filter(comment_to_post=comment)
        self.assertEqual(images.count(), 0)

    def test_create_comment_with_invalid_image(self):
        """Test creating a comment with an invalid image"""

        
        data = {
            'comment': 'This comment has an invalid image',
            'uploaded_comment_to_post_images': [generate_invalid_file()]
        }

        serializer = PostCommentSerializer(data=data, context={'post_id': self.post.id, 'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('uploaded_comment_to_post_images', serializer.errors)

    def test_create_comment_exceeding_image_limit(self):
        """Test creating a comment with more than allowed number of images"""

        data = {
            'comment': 'This comment exceeds image limit',
            'uploaded_comment_to_post_images': [generate_image_file(), generate_image_file(), generate_image_file()]
        }

        serializer = PostCommentSerializer(data=data, context={'post_id': self.post.id, 'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('uploaded_comment_to_post_images', serializer.errors)
        self.assertIn('Ensure this field has no more than 2 elements.', serializer.errors['uploaded_comment_to_post_images'][0])
        

class PostReactionSerializerTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_create_post_reaction(self):
        """Test creation of post reaction"""

        self.request = self.factory.post('/') 
        self.request.user = self.user
        valid_data = {
            'post': self.post.id,
            'reaction': 'upvote'
        }

        serializer = PostReactionSerializer(data=valid_data, context={'request': self.request})
        self.assertTrue(serializer.is_valid())
        post_reaction = serializer.save()
        
        self.assertEqual(post_reaction.reaction, valid_data['reaction'])
        self.assertEqual(post_reaction.post, self.post)
        self.assertEqual(post_reaction.user_that_react, self.user)

    # def test_update_post_reaction(self):
    #     existing_reaction = PostReactionFactory(post=self.post, user_that_react=self.user, reaction='like')
        
    #     data = {
    #         'post': self.post.id,
    #         'reaction': 'dislike'
    #     }
    #     serializer = PostReactionSerializer(data=data, context={'request': self.request})
    #     self.assertTrue(serializer.is_valid())
    #     post_reaction = serializer.save()
        
    #     self.assertEqual(post_reaction.reaction, 'dislike')
    #     self.assertEqual(post_reaction.post, self.post)
    #     self.assertEqual(post_reaction.user_that_react, self.user)
    #     self.assertEqual(PostReaction.objects.count(), 1)  # Ensure it didn't create a new entry



