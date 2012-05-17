import os, sys

path = '/Users/brab/Sites'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jotter.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

