from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError
from tests.accounts.factories import UserFactory


User = get_user_model()



class TestCustomUserModel(TestCase):

    def setUp(self):
        self.user = UserFactory(email='delight@mail.com', password='delightpassword', username='delight')
        self.user.set_password(self.user.password)
        self.user.save()


    def test_custom_user_creation(self):
        """Test if a CustomUser instance is created correctly"""
        self.assertEqual(self.user.username, 'delight')
        self.assertTrue(self.user.check_password('delightpassword'))

    def test_custom_user_str_method(self):
        """Test the __str__ method of the CustomUser model"""
        self.assertEqual(str(self.user), self.user.username)

    def test_custom_user_email_uniqueness(self):
        """Test the unique constraint on the email field"""
        user = UserFactory.build(email=self.user.email, username='user')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_custom_user_email_field_length(self):
        """Test the max length of the email field"""
        user = UserFactory(email='a' * 21 + '@mail.com', username='user')
        with self.assertRaises(ValidationError):
            user.full_clean()

