from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from atw.views import HomePageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^u/', include('utopia.urls')),
    url(r'^templatejs/', include('templatejs.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)
