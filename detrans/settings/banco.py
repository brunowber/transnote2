"""Banco"""

from detrans.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'detrans1',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '191.52.62.55',
        'PORT': '5432',
    }
}
