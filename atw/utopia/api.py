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
from django.template.defaultfilters import date as _date

from utopia.models import *

from magic import Magic
from os import path
import markdown2 as md


from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

magic_mime = Magic(mime=True)
def get_mime(fp):
    ret = magic_mime.from_file(path.join(settings.MEDIA_ROOT, fp))
    #print '%s %s %s'%(settings.MEDIA_ROOT, fp, ret)
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
        detail_allowed_methods = ['get', 'post']
        
    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(pk=request.user.pk)
        
class UserProfileResource(ModelResource):
    #user = fields.ToOneField(to='utopia.api.UserResource', attribute='user')
    first_name = fields.CharField()
    last_name = fields.CharField()
    
    class Meta:
        always_return_data = True
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'
        excludes = ['email', 'password', 'is_superuser']
        # Add it here.
        authentication = SessionAuthentication()
        authorization = UserObjectsOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get','put']
    
    def dehydrate_first_name(self, bundle):
        return bundle.obj.user.first_name
        
    def dehydrate_last_name(self, bundle):
        return bundle.obj.user.last_name
    
    def obj_update(self, bundle, **kwargs):
        ret =  super(UserProfileResource, self).obj_update(bundle, **kwargs)
        try:
            u = bundle.obj.user
            u.first_name = bundle.data['first_name']
            u.last_name = bundle.data['last_name']
            u.save()
        except Exception:
            print 'could not get the user from obj'
        return ret
    
    def get_object_list(self, request):
        q = super(UserProfileResource, self).get_object_list(request)
        fq = q.filter(user=request.user)
        return fq

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
        authorization = UserObjectsOnlyAuthorization()

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
   
    def dehydrate_body(self, bundle):
        try:
            return md.markdown(bundle.obj.body)
        except Exception:
            pass
        return ''

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
            
        
class EventResource(ModelResource):
    class Meta:
        always_return_data = True
        queryset = Event.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        authorization = DjangoAuthorization()
        
    start = fields.CharField()
    end = fields.CharField()
    
    def dehydrate_start(self, bundle):
        return _date(bundle.obj.start_date, 'N j, Y')
        
    def dehydrate_end(self, bundle):
        return _date(bundle.obj.end_date, 'N j, Y')
    