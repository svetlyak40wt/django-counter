from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^c/(?P<ctype_id>\d+)/(?P<object_id>\d+)/$', 'counter.views.count'),
     (r'^r/(?P<counter_id>\d+)/$', 'counter.views.redir'),
)
