from django.conf.urls.defaults import *


urlpatterns = patterns('',

    (r'^(?P<url>.*)$', 'verdjnlib.templatepages.views.templatepage'),

)
