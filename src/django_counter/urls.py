from django.conf.urls.defaults import *

urlpatterns = patterns('django_counter.views',
     (r'^c/(?P<ctype_id>\d+)/(?P<object_id>\d+)/$', 'count', {}, 'django-counter-count'),
     (r'^r/(?P<counter_id>\d+)/$', 'redir', {}, 'django-counter-redir'),
)

