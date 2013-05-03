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

from utopia.models import Episode, Media

models.signals.post_save.connect(create_api_key, sender=User)

class EpisodeResource(ModelResource):
    medias = fields.ToManyField('utopia.api.MediaResource', 'medias', null=True)

    class Meta:
        always_return_data = True
        queryset = Episode.objects.all()
        resource_name = 'episode'
        #excludes = []
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
   
   

class MediaResource(ModelResource):
    episode = fields.ToOneField(EpisodeResource, 'episodes')
    
    class Meta:
        always_return_data = True
        queryset = Media.objects.all()
        
