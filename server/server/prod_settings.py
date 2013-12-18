import os
ANGULAR_ROOT = os.path.realpath(os.path.join('.', '../dist'))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'ec2-107-22-170-211.compute-1.amazonaws.com',
        'NAME': 'd80965fsrp8nop',
        'PASSWORD': 'i3l8f3rKfd17OkJWHxST0VGJrA',
        'PORT': 5432,
        'USER': 'fqqkklfpjudklx',
    },
}
