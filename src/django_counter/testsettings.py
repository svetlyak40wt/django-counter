DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/django.db'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_counter',
]
ROOT_URLCONF = 'django_counter.urls'
TEMPLATE_DIRS = (
    'src/django_counter/test_templates',
)
