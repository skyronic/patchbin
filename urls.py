from django.conf.urls.defaults import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'patchbin.core.views.index'),
    (r'^submit$', 'patchbin.core.views.submit'),
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<urlCode>[A-Za-z0-9]{6})$', 'patchbin.diffviewer.views.showpatch'),
    (r'^(?P<urlCode>[A-Za-z0-9]{6})/newcomment$',
     'patchbin.diffviewer.views.newcomment'),
    (r'about/', 'patchbin.core.views.about'),
    (r'contribute/', 'patchbin.core.views.contribute'),
    (r'sponsor/', 'patchbin.core.views.sponsor')
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/anirudhs/Projects/patchbin/static'}))
