from rest_framework import serializers
from django.contrib.auth import get_user_model
from blog.accounts.api.v1.serializers import (
    SignUpSerializer,
    SignInSerializer,
    ChangePasswordSerializer,
    UserSerializer
)
from rest_framework.test import APITestCase, APIRequestFactory
from tests.accounts.factories import UserFactory
from unittest import mock

User = get_user_model()


class TestUserSignUpSerializer(APITestCase):

    def setUp(self):
        self.maxDiff = None
        
    def test_serializer_with_valid_data(self):
        valid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delightboy',
            'email': 'delight@mail.com',
            'password': 'delightpassword'
        }

        serializer = SignUpSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        
        user = User.objects.get(username=valid_data['username'])
        self.assertEqual(user.first_name, valid_data['first_name'])
        self.assertEqual(user.last_name, valid_data['last_name'])
        self.assertEqual(user.username, valid_data['username'])
        self.assertEqual(user.email, valid_data['email'])
        self.assertTrue(user.check_password(valid_data['password']))

    def test_serializer_with_invalid_data(self):
        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'email': 'delightail.com',  
            'password': 'delightpassword'
        }

        serializer = SignUpSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_serializer_with_existing_email(self):
        UserFactory(email='delight@mail.com')

        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delightboy',
            'email': 'delight@mail.com',  
            'password': 'delightpassword'
        }
       
        serializer = SignUpSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_serializer_with_existing_username(self):
        UserFactory(username='delight')
        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'email': 'delightail.com',  
            'password': 'delightpassword'
        }

        
        serializer = SignUpSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)


class TestSignInSerializer(APITestCase):

    def setUp(self):
        self.user = UserFactory(email='john@mail.com')
        self.user.set_password('johnpassword')
        self.user.save()

    @mock.patch('rest_framework_simplejwt.tokens.RefreshToken.for_user')
    def test_sign_in_serializer_with_valid_credentials(self, mock_for_user):
        """Test SignInSerializer with valid credentials"""

        valid_data = {
            'email_or_username': self.user.email,
            'password': 'johnpassword'
        }

        mock_tokens = mock.MagicMock()
        mock_tokens.access_token = '1896463823792'
        mock_tokens.__str__.return_value = '1896466142448'
        mock_for_user.return_value = mock_tokens

        serializer = SignInSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        response_data = serializer.data
        self.assertEqual(response_data['refresh_token'], str(mock_for_user.return_value))
        self.assertEqual(response_data['access_token'], mock_for_user.return_value.access_token)

    def test_sign_in_serializer_with_invalid_credentials(self):
        """Test SignInSerializer with invalid credentials"""

        invalid_data = {
            'email_or_username': self.user.email,
            'password': 'wrongpassword'
        }

        serializer = SignInSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['message'][0], 'Invalid Password')

    def test_sign_in_serializer_with_non_existing_user(self):
        """Test SignInSerializer with non-existing user"""

        non_existing_data = {
            'email_or_username': 'unknownuser@mail.com',
            'password': 'unknownuserpassword'
        }

        serializer = SignInSerializer(data=non_existing_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors['message'][0], "User doesn't exist")


class TestChangePasswordSerializer(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(email='delight@mail.com')
        self.user.set_password('delightpassword')
        self.user.save()

    def test_valid_data_changes_password(self):
        """Test that valid data changes the password successfully"""
        
        request = self.factory.put('/')
        request.user = self.user
        valid_data = {
            'old_password': 'delightpassword',
            'new_password': 'newdelightpassword',
            'confirm_password': 'newdelightpassword'
        }

        serializer = ChangePasswordSerializer(data=valid_data, context={'request': request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(valid_data['confirm_password']))  # Check the new password

    def test_mismatched_passwords(self):
        """Test that mismatched new password and confirm password raises error"""
        request = self.factory.put('/')
        request.user = self.user
        invalid_data = {
            'old_password': 'delightpassword',
            'new_password': 'newdelightpassword',
            'confirm_password': 'differentpassword'
        }

        serializer = ChangePasswordSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('message', serializer.errors)
        self.assertEqual(serializer.errors['message'][0], "New password not same as confirm password")

    def test_new_password_same_as_old_password(self):
        """Test that new password same as old password raises error"""
        request = self.factory.put('/')
        request.user = self.user
        invalid_data = {
            'old_password': 'delightpassword',
            'new_password': 'delightpassword',
            'confirm_password': 'delightpassword'
        }

        serializer = ChangePasswordSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('messsage', serializer.errors)
        self.assertEqual(serializer.errors['messsage'][0], "New pasword can't be same old password")

    def test_invalid_old_password(self):
        """Test that incorrect old password raises error"""
        request = self.factory.put('/')
        request.user = self.user
        invalid_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newdelightpassword',
            'confirm_password': 'newdelightpassword'
        }

        serializer = ChangePasswordSerializer(data=invalid_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('message', serializer.errors)
        self.assertEqual(serializer.errors['message'][0], "Invalid old password")  

        
class TestUpdateProfileSerializer(APITestCase):

    def setUp(self):
        self.user = UserFactory(email='delight@mail.com')
        self.factory = APIRequestFactory()
        self.request = self.factory.put('/')


    def test_valid_data_updates_profile(self):
        """Test that valid data updates the user's profile successfully"""
        self.request.user = self.user
                        
        valid_data = {
            'first_name': 'brown',
            'last_name': 'james',
            'username': 'jamesbrown'
        }

        serializer = UserSerializer(instance=self.user, data=valid_data, context={'request': self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, valid_data['first_name'])
        self.assertEqual(self.user.last_name, valid_data['last_name'])
        self.assertEqual(self.user.username, valid_data['username'])

    def test_username_unique_validation(self):
        """Test that changing username to an existing username raises an error"""
        self.request.user = self.user
        existing_user = UserFactory(username='existing_username')

        invalid_data = {
            'first_name': 'brown',
            'last_name': 'james',
            'username': 'existing_username'
        }

        serializer = UserSerializer(instance=self.user, data=invalid_data, context={'request': self.request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.username, invalid_data['username'])
