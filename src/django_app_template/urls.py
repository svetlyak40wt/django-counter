from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^/$', 'django_app_template.views.empty_view'),
)
