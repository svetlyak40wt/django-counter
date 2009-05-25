from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^/$', 'django_counter.views.empty_view'),
)
