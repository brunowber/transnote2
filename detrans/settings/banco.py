"""Banco"""

from detrans.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'user_db',
        'PASSWORD': 'password_db',
        'HOST': 'host_db',
        'PORT': 'port_db',
    }
}
