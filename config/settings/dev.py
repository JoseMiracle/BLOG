from .base import *
from datetime import timedelta

ALLOWED_HOSTS = ['localhost']

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "drf_standardized_errors",
    "django_filters",
]

LOCAL_APPS = [
    "blog.accounts",
    "blog.posts",
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2, 
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',              
#         'USER': 'postgres',              
#         'PASSWORD': 'postgres',      
#         'HOST': 'postgres_db',                 
#         'PORT': '5432',                          
#     }
# }




SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

AUTH_USER_MODEL = 'accounts.CustomUser'

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'