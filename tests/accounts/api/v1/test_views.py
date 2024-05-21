from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from tests.accounts.factories import UserFactory
from unittest import mock
from unittest.mock import MagicMock

User = get_user_model()


class TestSignUpAPIView(APITestCase):
    
    def setUp(self):
        self.url = reverse('accounts:sign_up')

    
    def test_account_is_created_when_valid_data_are_provided(self):
        """Test that account is created when valid data are provided"""

        valid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delightboy',
            'email': 'delight@mail.com',
            'password': 'delightpassword'
        }

        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, 201)

        user =  User.objects.filter(email=valid_data['email']).first()
        self.assertIsNotNone(user)
        self.assertTrue(check_password(valid_data['password'], user.password))
        self.assertEqual(valid_data['email'], user.email)

    def test_account_is_not_created_when_invalid_data_are_provided(self):
        """Test account is not created when invalid data are provided"""

        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delightboy',
            'email': 'delightail.com',
            'password': 'delightpassword'
        }

        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)

        user = User.objects.filter(email=invalid_data['email']).first()
        self.assertIsNone(user)
    
    def test_account_can_only_be_created_for_one_email_address(self):
        """Test account can only be created for one email address alone"""
        
        existing_user = UserFactory(email='delight@mail.com')

        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delightboy',
            'email': 'delight@mail.com',
            'password': 'delightpassword'
        }

        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        
        user = User.objects.filter(email=invalid_data['email']).count()
        self.assertEqual(user, 1)
    
    def test_account_not_created_when_existing_username_is_provided(self):
        """Test account is not created when existing username is provided"""


        existing_user = UserFactory(username='delight')
        
        invalid_data = {
            'first_name': 'Delight',
            'last_name': 'John',
            'username': 'delight',
            'email': 'delight@mail.com',
            'password': 'delightpassword'
        }

        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        
        user = User.objects.filter(username=invalid_data['username']).count()
        self.assertEqual(user, 1)



class TestSignInAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:sign_in')
        self.user = UserFactory(email='john@mail.com')
        self.user.set_password('johnpassword')
        self.user.save()

        
    @mock.patch('blog.accounts.api.v1.serializers.RefreshToken.for_user')
    def test_account_is_signed_in_when_valid_credentials_are_provided(self, mock_for_user):
        """Test account is signed in if valid crredentials are provided"""

        valid_data = {
            'email_or_username': self.user.email,
            'password': 'johnpassword'
        }
        self.user.refresh_from_db()


        mock_tokens = MagicMock()
        mock_tokens.access_token = '1896463823792'
        mock_tokens.__str__.return_value = '1896466142448'
        mock_for_user.return_value = mock_tokens


        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()['refresh_token'], str(mock_for_user.return_value))
        self.assertEqual(response.json()['access_token'], mock_for_user.return_value.access_token)


    def test_account_not_signed_in_when_invalid_credentials_are_provided(self):
        """Test account isn't signed in when invalid credentials are provided"""

        invalid_data = {
            'email_or_username': self.user.email,
            'password': 'wrongpassword'
        }        

        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('refresh_token', response.json())
    
    def test_non_existing_account_cannot_be_signed_in(self):
        """Test non-existing account cannot be signed in"""

        invalid_data = {
            'email_or_username': 'unknownuser@mail.com',
            'password': 'unknownuserpassword'
        }

        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0]['detail'], "User doesn't exist")




class TestChangePasswordAPIView(APITestCase):
    
    def setUp(self):
        self.url = reverse('accounts:change_password')
        self.user = UserFactory(email='delight@mail.com')
        self.user.set_password('delightpassword')
        self.user.save()


    def test_authenticated_can_change_password(self):
        """Test authenticated user can change their password"""

        self.client.force_authenticate(self.user)

        valid_data = {
            'old_password': 'delightpassword',
            'new_password': 'newdelightpassword',
            'confirm_password': 'newdelightpassword'
        }

        response = self.client.put(self.url, valid_data, format='json')

        self.assertEqual(response.status_code, 200)

        self.assertTrue(self.user.check_password(valid_data['confirm_password']))

    
    def test_unautheticated_user_cannot_change_their_password(self):
        """ Test unauthenticated user cannot change their password"""

        invalid_data = {
            'old_password': 'delightpassword',
            'new_password': 'newdelightpassword',
            'confirm_password': 'newdelightpassword'
        }

        response = self.client.put(self.url, invalid_data, format='json')

        self.assertEqual(response.status_code, 401)

    
    def test_authenticated_user_password_remains_unchanged_when_invalid_data_is_provided(self):
        """Test authenticated user password not changed when invalid data is provided"""

        self.client.force_authenticate(self.user)

        invalid_data = {
            'old_password': 'password',
            'new_password': 'newdelightpassword',
            'confirm_password': 'newdelightpassword'
        }

        response = self.client.put(self.url, invalid_data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertTrue(self.user.check_password('delightpassword'))


class TestRetrieveUpdateProfileAPIView(APITestCase):

    def setUp(self):
        self.url = reverse('accounts:retrieve_update_profile')
        self.user = UserFactory(email='delight@mail.com')


    def test_authenticated_user_can_update_their_profile_with_valid_data(self):
        """Test authenticated use fcan update their profiel with valid data"""
        
        self.client.force_authenticate(self.user)
        valid_data = {
            'first_name': 'brown',
            'last_name': 'james',
            'username': 'jamesbrown'
        }

        response = self.client.put(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.first_name, valid_data['first_name'])
        self.assertEqual(self.user.last_name, valid_data['last_name'])
        self.assertEqual(self.user.username, valid_data['username'])

    
    def test_unauthenticated_user_cannot_update_their_profile(self):
        """Test unauthenticated use fcan update their profile with valid data"""
        
        invalid_data = {
            'first_name': 'brown',
            'last_name': 'james',
            'username': 'jamesbrown'
        }

        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 401)

        self.assertNotEqual(self.user.first_name, invalid_data['first_name'])
        self.assertNotEqual(self.user.last_name, invalid_data['last_name'])
    
    def test_authenticated_user_can_retrieve_their_profile(self):
        """Test authenticated user can retrieve their profile"""

        self.client.force_authenticate(self.user)

        expected_response = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'image': None
        }

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(expected_response, response.json())




    
    def authenticated_user_cannot_change_their_username_to_an_existing_username_when_updating_profile(self):
        """Test authenticated user cannot change their username to an existing username when updating profile"""
        
        self.client.force_authenticate(self.user)

        existing_user = UserFactory(email='existing_username')

        invalid_data = {
            'first_name': 'brown',
            'last_name': 'james',
            'username': 'existing_username'
        }

        response = self.client.put(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(self.user.username, invalid_data['username'])





