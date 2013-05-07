# -*- coding: utf-8 -*-
"""
utopia.api
"""


from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from django.conf import settings

from utopia.models import *

from magic import Magic
from os import path

magic_mime = Magic(mime=True)
def get_mime(fp):
    ret = magic_mime.from_file(path.join(settings.MEDIA_ROOT, fp))
    print '%s %s %s'%(settings.MEDIA_ROOT, fp, ret)
    return ret

models.signals.post_save.connect(create_api_key, sender=User)

class EpisodeResource(ModelResource):
    medias = fields.ToManyField(to='utopia.api.MediaResource', attribute='media_set', null=True)

    class Meta:
        always_return_data = True
        queryset = Episode.objects.all()
        resource_name = 'episode'
        #excludes = []
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
   
   

class MediaResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Media.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        
    episode = fields.ToOneField(to='utopia.api.EpisodeResource', attribute='episode', null=True, blank=True)
    mime = fields.CharField()
        
    def dehydrate_mime(self, bundle):
        T, ST = list(get_mime(bundle.obj.resource.file.name).split('/'))
        print '%s %s/%s'%(bundle.obj.resource.file.name,T,ST)
        if ST == 'webm':
            if T == 'video':
                ST = 'webmv'
            else:
                ST = 'webma'
        if ST == 'ogg':
            if T == 'audio':
                ST = 'oga'
            else:
                ST = 'ogv'
        return '/'.join([T,ST])
        
        


class HomeImageResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = HomeImage.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        
    def dehydrate_image(self, bundle):
        return bundle.obj.image.url
            
        
        