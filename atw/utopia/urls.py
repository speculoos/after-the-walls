from django.conf.urls import patterns, include, url
from tastypie.api import Api

from utopia.api import *

api = Api(api_name='api')
api.register(EpisodeResource())
api.register(MediaResource())
api.register(HomeImageResource())
api.register(MessageResource())

urlpatterns = patterns('utopia',
    (r'', include(api.urls)),
)
