"""Banco"""

from detrans.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'db_name',
        'NAME': 'postgres',
        'USER': 'postgres',
        # 'USER': 'user_db',
        'PASSWORD': 'postgres',
        # 'PASSWORD': 'password_db',
        'HOST': '191.52.62.38',
        # 'HOST': 'host_db',
        'PORT': '5432',
        # 'PORT': 'port_db',
    }
}
