from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'patchbin.core.views.index'),
    (r'^submit$', 'patchbin.core.views.submit'),
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<urlCode>[A-Za-z0-9]{6})$', 'patchbin.core.views.showpatch')
)
