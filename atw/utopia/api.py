# -*- coding: utf-8 -*-
"""
utopia.api
"""


from tastypie import fields
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import SessionAuthentication
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.models import create_api_key

from django.contrib.auth.models import User
from django.db import models
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

class UserResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

class MessageResource(ModelResource):
    user = fields.ToOneField(to='utopia.api.UserResource', attribute='user')
    
    def obj_create( self, bundle, **kwargs ):
        #print bundle
        u = User.objects.get(pk=bundle.data['user'])
        bundle.data['user'] = u
        super( MessageResource, self ).obj_create( bundle, **kwargs )
        
    def dehydrate_user(self, bundle):
        return bundle.obj.user.pk
        
    def get_object_list(self, request):
        return super(MessageResource, self).get_object_list(request).filter(user=request.user)

    class Meta:
        always_return_data = True
        queryset = Message.objects.all()
        resource_name = 'message'
        list_allowed_methods = ['get','post']
        detail_allowed_methods = ['get','post']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()

class EpisodeResource(ModelResource):
    media = fields.ToOneField(to='utopia.api.MediaResource', attribute='media', null=True, blank=True)

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
        
    mime = fields.CharField()
        
    def dehydrate_mime(self, bundle):
        T, ST = list(get_mime(bundle.obj.resource.file.name).split('/'))
        #print '%s %s/%s'%(bundle.obj.resource.file.name,T,ST)
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
            
        
        