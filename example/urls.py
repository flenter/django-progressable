from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import nexus
nexus.autodiscover()


urlpatterns = patterns('',
    url(r'^tsktsk', include('tsktsk.urls')),
    url(r'^api/', include('progressable.urls')),
    url(r'^admin_tools', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.urls')),

) + staticfiles_urlpatterns()
