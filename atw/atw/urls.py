from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from atw.views import HomePageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login$', 'atw.views.login', name='login'),
    url(r'^logout$', 'atw.views.logout', name='logout'),
    
    url(r'^register_step_0$', 'atw.views.register_step_0', name='register_step_0'),
    url(r'^register_step_1$', 'atw.views.register_step_1', name='register_step_1'),
    
    url(r'^u/', include('utopia.urls')),
    url(r'^templatejs/', include('templatejs.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )