from django.conf.urls import patterns, include, url
from tastypie.api import Api

from utopia.api import *

api = Api(api_name='api')
api.register(EpisodeResource())
api.register(MediaResource())

urlpatterns = patterns('utopia',
    (r'', include(api.urls)),
)
