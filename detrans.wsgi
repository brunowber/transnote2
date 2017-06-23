#encoding: utf-8
#apache_configuration = os.path.dirname(__file__)
#project = os.path.dirname(apache_configuration)
#workspace = os.path.dirname(project)
#sys.path.append(workspace)
#sys.path.append('/usr/local/lib/python2.7/dist-packages/django/')
#sys.path.append('/home/virtualenvs/ramais/local/lib/python2.7/site-packages/')
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
env = LC_ALL=pt_BR.UTF-8


import os, sys, site

# Activate your virtual env
activate_env=os.path.expanduser("/home/virtualenvs/detrans/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))


# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/virtualenvs/detrans/local/lib/python2.7/site-packages')

# Add the apps directory to the PYTHONPATH
sys.path.append('/var/www/detrans/')

#to set enviroment settings for Django apps
os.environ["DJANGO_SETTINGS_MODULE"] = "detrans.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


