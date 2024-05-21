from django.core.exceptions import ValidationError
from django.test import TestCase
from tests.posts.factories import (
    PostFactory,
    UserFactory,
    PostImageFactory,
    PostCommentFactory
)  
from blog.posts.models import (
    Post,
    PostComment,
    PostImage, 
    post_images_upload_location
)

class TestPostModel(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)

    def test_post_creation(self):
        """Test if a Post instance is created correctly"""
        self.assertIsInstance(self.post, Post)
        self.assertEqual(self.post.author, self.user)
        self.assertIn(self.post.category, [choice[0] for choice in Post.CATEGORY_CHOICES])

   

    def test_post_category_choices(self):
        """Test the category field choices"""
        with self.assertRaises(ValidationError):
            self.post.category = 'invalid_category'
            self.post.full_clean()

    def test_post_state_choices(self):
        """Test the post_state field choices"""
        with self.assertRaises(ValidationError):
            self.post.post_state = 'invalid_state'
            self.post.full_clean()
    
    def test_post_creation_with_specific_data(self):
        """Test creating a Post with specific data"""
        post = PostFactory(title='A Specific Title', author=self.user, content='Specific content', post_state='published', category='education')
        self.assertEqual(post.title, 'A Specific Title')
        self.assertEqual(post.content, 'Specific content')
        self.assertEqual(post.post_state, 'published')
        self.assertEqual(post.category, 'education')


class TestPostImageModel(TestCase):

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.post_image = PostImageFactory(post=self.post)

    def test_post_image_creation(self):
        """Test if a PostImage instance is created correctly"""
        self.assertIsInstance(self.post_image, PostImage)
        self.assertEqual(self.post_image.post, self.post)
        self.assertTrue(self.post_image.image.name.startswith('posts/images/'))

    def test_post_image_upload_location(self):
        """Test the upload location for the image field"""
        filename = self.post_image.image.name.split('/')[-1]
        expected_path = f'posts/images/{filename}'
        self.assertEqual(self.post_image.image.name, expected_path)

    def test_post_images_upload_location_function(self):
        """Test the post_images_upload_location function"""
        filename = 'sample_image.jpg'
        expected_path = f'posts/images/{filename}'
        actual_path = post_images_upload_location(None, filename)
        self.assertEqual(expected_path, actual_path)

class TestPostCommentModel(TestCase):

    def setUp(self):
        self.user = UserFactory(email='brown@mail.com', username='brown')
        self.post = PostFactory(author=self.user)
        self.comment = "This is a test comment."
        self.user_that_comment = UserFactory(email='anotheruser@mail.com', username='anotheruser')
        self.post_comment = PostCommentFactory(post=self.post, user_that_comment=self.user_that_comment, comment=self.comment)
        self.child_comment = PostCommentFactory(post=self.post, user_that_comment=self.user_that_comment, comment="Child comment", parent_comment=self.post_comment)

    def test_post_comment_creation(self):
        """Test if a PostComment instance is created correctly"""
        self.assertIsInstance(self.post_comment, PostComment)
        self.assertEqual(self.post_comment.post, self.post)
        self.assertEqual(self.post_comment.user_that_comment, self.user_that_comment)
        self.assertEqual(self.post_comment.comment, self.comment)

    def test_post_comment_str_method(self):
        """Test the __str__ method of the PostComment model"""
        expected_str = self.comment[:20]
        self.assertEqual(str(self.post_comment), expected_str)

    def test_post_comment_without_parent(self):
        """Test PostComment creation without a parent comment"""
        independent_comment = PostCommentFactory(post=self.post, user_that_comment=self.user, comment="Independent comment", parent_comment=None)
        self.assertIsNone(independent_comment.parent_comment)
        self.assertEqual(independent_comment.comment, "Independent comment")