from tests.posts.factories import (
    PostFactory, 
    PostCommentFactory,
    PostReactionFactory
)
from tests.accounts.factories import UserFactory
from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.utils import generate_image_file
from blog.posts.models import (
    Post, 
    PostImage,
    PostComment, 
    CommentToPostImages,
    PostReaction
)

User = get_user_model()




class TestCreatePostAPIView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.url = reverse('posts:create_post')
    

    def test_authenticated_user_can_make_post(self):
        """Test authenticated user can make post"""

        self.client.force_authenticate(self.user)
        request = self.factory.post('/')
        request.user  = self.user
        
        valid_data = {
            'title': 'Love a dog',
            'post_state': 'published',
            'content': "My love for dog is undisputed",
            'category': 'lifestyle',
            'uploaded_images': [generate_image_file()]
        }

        response = self.client.post(self.url, valid_data, format='multipart', context={'request': request})
        self.assertEqual(response.status_code, 201)
       
        post = Post.objects.filter(author=self.user).first()
        self.assertIsNotNone(post)
        self.assertEqual(post.title, valid_data['title'])

    
    def test_unauthenticated_user_cannot_make_post(self):
        """Test unauthenticated user cannot make post"""
        
        invalid_data = {
            'title': 'Love a dog',
            'post_state': 'published',
            'content': "My love for dog is undisputed",
            'category': 'lifestyle',
            'uploaded_images': [generate_image_file()]
        }

        response = self.client.post(self.url, invalid_data, format='multipart')
        self.assertEqual(response.status_code, 401)

    
    def test_authenticated_user_can_upload_multiple_images_with_post(self):
        """Test authenticated user can upload multiple images with post"""

        self.client.force_authenticate(self.user)
        request = self.factory.post('/')
        request.user  = self.user


        valid_data = {
            'title': 'Read good books',
            'post_state': 'published',
            'content': "I love reading books",
            'category': 'lifestyle',
            'uploaded_images': [generate_image_file(), generate_image_file()]
        }

        response = self.client.post(self.url, valid_data, format='multipart', context={'request': request})
        self.assertEqual(response.status_code, 201)
        post = Post.objects.filter(author=self.user).first()
        post_images = PostImage.objects.filter(post=post)
        
        self.assertIsNotNone(post)
        self.assertEqual(post.title, valid_data['title'])
        self.assertEqual(post_images.count(), 2)


class TestUpdatePostAPIView(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory(author=self.user, title='my first post')

    
    def test_authenticated_user_can_update_to_their_post(self):
        """Test authenticated user can update to their post"""

        url = reverse('posts:update_post', args=[self.post.id])
        self.client.force_authenticate(self.user)

        valid_data = {
            'title': 'New Title',
            'content': 'No content for now',
            'category': self.post.category
        }
        response = self.client.put(url,  valid_data, format='json')
        self.assertEqual(response.status_code, 200)

        self.post.refresh_from_db()

        self.assertEqual(self.post.title, valid_data['title'])

    
    def test_another_user_cannot_update_another_user_post(self):
        """Test another user cannot update another user post"""

        another_user = UserFactory(email='anotheruser@mail.com', username='anotheruser')
        self.client.force_authenticate(another_user)

        invalid_data = {
            'title': 'New Title',
            'content': 'No content for now',
            'category': self.post.category
        }

        url = reverse('posts:update_post', args=[self.post.id])
        response = self.client.put(url, invalid_data, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.post.title, 'my first post')



class TestDeletePostAPIView(APITestCase):

    def setUp(self):
        self.user = UserFactory(email='mimi@mail.com') 
        self.post = PostFactory(author=self.user)

    def test_authenticated_owner_of_a_post_can_delete_their_post(self):
        """Test authenticated owner of a post can delete their post"""

        self.client.force_authenticate(self.user)
        url = reverse('posts:delete_post', args=[self.post.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        post = Post.objects.filter(id=self.post.id).first()
        self.assertIsNone(post)
    
    def test_another_authenticated_user_cannot_delete_another_user_post(self):
        """Test another user cannot delete another user post"""

        another_user = UserFactory(email='anotheruser@mail.com', username='anotheruser')
        self.client.force_authenticate(another_user)
        url = reverse('posts:delete_post', args=[self.post.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        post = Post.objects.filter(id=self.post.id).first()
        self.assertIsNotNone(post)

class TestUserPostsAPIView(APITestCase):
    
    def setUp(self):
        self.url = reverse('posts:user_posts')
        self.user = UserFactory()
        self.user_draft_posts = PostFactory.create_batch(author=self.user, size=2, post_state='draft')
        self.user_published_posts = PostFactory.create_batch(author=self.user, size=2, post_state='published')

    
    
    def test_authenticated_user_can_view_their_posts(self):
        """Test authenticated user can view their posts"""
        
        self.client.force_authenticate(self.user)
        
        response = self.client.get(self.url)
        self.assertEqual(response.json()['count'], 4)
        self.assertEqual(len(response.json()['results']), 2)     
    
    
    def test_another_authenticated_user_cannot_view_draft_and_published_posts_that_isnt_their_own(self):
        """Test another authenticated user cannot view draft and published posts that isn't their own"""

        another_user = UserFactory(email='anotheruser@mail.com', username='anotheruser')
        self.client.force_authenticate(another_user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        self.assertEqual(len((response.json()['results'])), 0)
    

class TestPublishedPostAPIview(APITestCase):

    def setUp(self):
        self.another_user = UserFactory(email='delight@mqil.com', username='delight')
        self.user_published_posts = PostFactory.create_batch(author=self.another_user, size=3, post_state='published')
        self.user_draft_posts =  PostFactory.create_batch(author=self.another_user, size=2, post_state='drafts')

    
    def test_authenticated_user_can_view_another_user_posts(self):
        """Test authenticated user can view another user's posts"""
        
        url =  reverse('posts:user_published_posts', args=[self.another_user.username])
        user = UserFactory(email='user@mail.com', username='user')

        self.client.force_authenticate(user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3) # NOTE: number of published post
    
    def test_unauthenticated_cannot_view_user_posts(self):
        
        """ Test unauthenticated user cannot view user posts"""
        url =  reverse('posts:user_published_posts', args=[self.another_user.username])
        user = UserFactory(email='user@mail.com', username='user')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

class TestAllPostAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('posts:all_posts')
        self.user = UserFactory(email='user@mail.com', username='user')
        self.another_user = UserFactory(email='anotheruser@mail.com', username='another')
        self.user_posts = PostFactory.create_batch(author=self.user, size=3, post_state='published', title='Why love dogs ?')
        self.another_user_posts = PostFactory.create_batch(author=self.another_user, size=4,  post_state='published', title='Read Today')


    
    def test_authenticated_user_can_all_view_posts(self):
        """Test authenticated user can view all posts"""

        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['count'], 7)
    
    
    def test_authenticated_user_can_search_for_post_by_username(self):
        """Test authenticated user can search for post by username"""

        search_url = f"{self.url}?search={self.user.username}"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)

        for result in response.json()['results']:
            self.assertEqual(result['author']['username'], self.user.username)
    

    def test_authenticated_user_can_search_for_by_title(self):
        """Test authenticated user can search for posts by title"""

        title = 'Read Today'
        search_url = f"{self.url}?search={title}"
        response = self.client.get(search_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 4)

        for result in response.json()['results']:
            self.assertEqual(result['title'], title)


class TestPostCommentAPIView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.post = PostFactory(author=self.user)
    

    def test_authenticated_user_can_comment_on_a_post(self):
        """Test authenticated user can comment on a post"""
        url = reverse('posts:post_comment', args=[self.post.id])
        request = self.factory.post('/')
        user_to_comment = UserFactory(email='user_to_comment@mail.com', username='userToComment')
        self.client.force_authenticate(user_to_comment)

        request.user = user_to_comment
      
        valid_data = {
            'comment': 'I love this post',
            'uploaded_comment_to_post_images': [generate_image_file(), generate_image_file()]
        }
        
        response = self.client.post(url, valid_data, format='multipart', context={'request': request})

        self.assertEqual(response.status_code, 201)
        post_comment = PostComment.objects.filter(post=self.post, user_that_comment=user_to_comment).first()

        self.assertIsNotNone(post_comment)
        comment_to_post_images = CommentToPostImages.objects.filter(comment_to_post=post_comment)

        self.assertEqual(comment_to_post_images.count(), len(valid_data['uploaded_comment_to_post_images']))

    
    def test_unauthenticated_user_cannot_comment_to_post(self):
        """Test unauthenticated user cannot comment to post"""

        url = reverse('posts:post_comment', args=[self.post.id])

        valid_data = {
            'comment': 'I love this post',
            'uploaded_comment_to_post_images': [generate_image_file(), generate_image_file()]
        }
        
        response = self.client.post(url, valid_data, format='multipart')

        self.assertEqual(response.status_code, 401)
        number_of_post_comment = PostComment.objects.count()
        self.assertEqual(number_of_post_comment, 0)
    
    def test_authenticated_user_can_post_comment_without_images(self):
        """Test authenticated user can post images without images"""

        url = reverse('posts:post_comment', args=[self.post.id])
        request = self.factory.post('/')
        user_to_comment = UserFactory(email='user_to_comment@mail.com', username='userToComment')
        self.client.force_authenticate(user_to_comment)

        request.user = user_to_comment
      
        valid_data = {
            'comment': 'I love this post',
        }
        
        response = self.client.post(url, valid_data, format='multipart', context={'request': request})

        self.assertEqual(response.status_code, 201)
        post_comment = PostComment.objects.filter(post=self.post, user_that_comment=user_to_comment).first()

        self.assertIsNotNone(post_comment)


class TestEditCommentAPIView(APITestCase):

    def setUp(self):
        self.user = UserFactory(email='user@mail.com', username='user')
        self.another_user = UserFactory(email='anotheruser@mail', username='anotheruser')
        self.post = PostFactory(author=self.user)
        self.post_comment = PostCommentFactory(post=self.post, user_that_comment=self.another_user, comment='I love this post')


    
    def test_authenticated_user_can_edit_their_comment(self):
        """Test authenticated user can edit their comment"""
        url = reverse('posts:edit_comment', args=[self.post_comment.id])
        self.client.force_authenticate(self.another_user)

        valid_data = {
            'comment': "I don't think I like this post"
        }

        response =  self.client.put(url, valid_data, format='json')

        self.assertEqual(response.status_code, 200)
        self.post_comment.refresh_from_db()
        self.assertEqual(self.post_comment.comment, valid_data['comment'])

    def test_only_owner_of_comment_can_update_their_comment(self):
        """Test only owner of comment can update therir comment"""

        url = reverse('posts:edit_comment', args=[self.post_comment.id])
        self.client.force_authenticate(self.user)

        valid_data = {
            'comment': "I don't think I like this post"
        }

        response =  self.client.put(url, valid_data, format='json')

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(self.post_comment.comment, valid_data['comment'])
    
    def test_unauthenticated_user_cannot_update_their_comment(self):
        """Test unauthenticated user cannot update their comment"""

        url = reverse('posts:edit_comment', args=[self.post_comment.id])

        valid_data = {
            'comment': "I don't think I like this post"
        }

        response =  self.client.put(url, valid_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertNotEqual(self.post_comment.comment, valid_data['comment'])


class TestPostReactionAPIView(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('posts:post_reaction')
        self.user = UserFactory(email='user@mail.com', username='user')
        self.post = PostFactory(author=self.user)

    
    def test_authenticated_user_can_react_to_post(self):
        """Test authenticated user can react to post"""
        request = self.factory.post('/')
        another_user = UserFactory(email='anotheruser@mail.com', username='anotheruser')
        self.client.force_authenticate(another_user)

        request.user = another_user


        valid_data = {
            'reaction': 'upvote',
            'post': self.post.id
        }

        response = self.client.post(self.url, valid_data, format='json', context={'request': request})

        self.assertEqual(response.status_code, 201)
        post_reaction = PostReaction.objects.filter(user_that_react=another_user, post=self.post).first()
        
        self.assertIsNotNone(post_reaction)
        self.assertEqual(post_reaction.reaction, valid_data['reaction'])

    
    def test_unauthenticated_user_cannot_react_to_post(self):
        """Test unauthenticated user cannot react to a post"""

        valid_data = {
            'reaction': 'upvote',
            'post': self.post.id
        }

        response = self.client.post(self.url, valid_data, format='json')

        self.assertEqual(response.status_code, 401)


class TestDeleteAPIView(APITestCase):

    def setUp(self):
        self.user = UserFactory(email='delight@mail.com', username='delight')
        self.post = PostFactory(author=self.user)
        self.post_reaction = PostReactionFactory(post=self.post, user_that_react=self.user)


    def test_authenticated_user_can_delete_their_post_reaction(self):
        """Test authenticated user can delete their post reaction"""

        self.client.force_authenticate(self.user)

        url = reverse('posts:delete_reaction', args=[self.post_reaction.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        number_of_reaction = PostReaction.objects.count()

        self.assertEqual(number_of_reaction, 0)
    
    def test_unauthenticated_user_cannot_delete_their_post_reaction(self):
        """Test aunauthenticated user cannot their post reaction"""

        url = reverse('posts:delete_reaction', args=[self.post_reaction.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401)

        number_of_reaction = PostReaction.objects.filter(user_that_react=self.user).count()

        self.assertEqual(number_of_reaction, 1)
    
    def test_another_user_cannot_delete_post_reaction_that_is_not_their_own(self):
        """Test another user cannot delete post reaction that is not their's"""

        another_user = UserFactory(email='anotheruser@mail.com', username='another_user')
        self.client.force_authenticate(another_user)

        url = reverse('posts:delete_reaction', args=[self.post_reaction.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

        number_of_reaction = PostReaction.objects.count()

        self.assertEqual(number_of_reaction, 1)
    









        




        




        




    





        



        




