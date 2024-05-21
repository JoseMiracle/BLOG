from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

User = get_user_model()



class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    first_name = "delight"
    last_name = "jose"
    email = "delight@gmail.com"
    is_active = True
    password = '123456789'
    username = 'delight'
