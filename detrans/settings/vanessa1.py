from base import *

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'detrans2',  # Or path to database file if using sqlite3.
        'USER': 'detrans',  # Not used with sqlite3.
        'PASSWORD': 'detrans.5@ifc',  # Not used with sqlite3.
        'HOST': '191.52.62.197',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',  # Set to empty string for default. Not used with sqlite3.
    }
}
