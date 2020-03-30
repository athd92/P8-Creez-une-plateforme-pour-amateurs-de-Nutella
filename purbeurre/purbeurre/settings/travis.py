from . import *

SECRET_KEY = 'ze4ouEZEDD(3Rdzzede$311&é'
DEBUG = False
ALLOWED_HOSTS = ['68.183.72.9']

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',        
        'NAME': 'purbeurredb',
        'USER': 'guest',
        'PASSWORD': 'password1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}