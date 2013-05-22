# -*- coding: utf-8 -*-
"""
utopia.models
"""

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.models import User

from adminsortable.models import Sortable

class UserProfile(models.Model):
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateur"
        permissions = (
            ("edit_own_profile", "Can edit own profile"),
            )
        
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile', verbose_name='Fou')
    title = models.CharField(verbose_name='Titre', max_length=32, blank=True, null=True, default=None)
    age = models.IntegerField(verbose_name='Age', blank=True, null=True, default=None)
    skills = models.CharField(verbose_name='Capacités', max_length=512, blank=True, null=True, default=None)
    interests = models.CharField(verbose_name='Interets', max_length=512, blank=True, null=True, default=None)
    city = models.CharField(verbose_name='Ville', max_length=512, blank=True, null=True, default=None)
    country = models.CharField(verbose_name='Pays', max_length=512, blank=True, null=True, default=None)
    languages = models.CharField(verbose_name='Langues', max_length=512, blank=True, null=True, default=None)
    
    def user_name(self):
        return self.user.get_full_name()
    
    def location(self):
        return u'%s, %s'%(self.city, self.country)
        
    def is_active(self):
        return self.user.is_active
    
    def __unicode__(self):
        return '%s <%s>'%(self.user.get_full_name(), self.user.email)

class Message(models.Model):
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        
    subject = models.SlugField(max_length=255, default='None')
    body = models.TextField(verbose_name='Corps',blank=True, null=True, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Fou')
    
    def __unicode__(self):
        return self.subject

class HomeImage(Sortable):
    class Meta(Sortable.Meta):
        verbose_name = "Image d'accueil"
        verbose_name_plural = "Images d'accueil"
    
    slug = models.SlugField(max_length=255, editable=False, default='None')
    image = models.ImageField(upload_to='home',  height_field='height', width_field='width', max_length=255);
    width = models.IntegerField(editable=False)
    height = models.IntegerField(editable=False)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.image)
        super(HomeImage, self).save(force_insert, force_update) 
    
    def __unicode__(self):
        return self.slug


class Media(models.Model):
    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Medias"
        ordering = ['name']
        
    slug = models.SlugField(max_length=1024, editable=False, default='None')
    name = models.CharField(verbose_name='Dénomination', max_length=1024)
    resource = models.FileField(upload_to='media', max_length=500)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Media, self).save(force_insert, force_update) 
        
        
    def __unicode__(self):
        return self.name

class Episode(models.Model):
    class Meta:
        verbose_name = "Épisode"
        verbose_name_plural = "Épisodes"
        ordering = ['pub_date']
        
        
    slug = models.SlugField(max_length=1024, editable=False, default='None')
    title = models.CharField(verbose_name='Titre', max_length=1024)
    body = models.TextField(verbose_name='Corps',blank=True, null=True, default=None)
    pub_date = models.DateField(blank=True, null=True, verbose_name='Date')
    media = models.ForeignKey('Media', verbose_name='Media', blank=True, null=True, default=None)
    
    bg_image = models.ImageField(upload_to='episode_bg', 
                                verbose_name='Image de fond',  
                                height_field='bg_height', 
                                width_field='bg_width', 
                                max_length=255,
                                blank=True, null=True, default=None);
    bg_width = models.IntegerField(editable=False, blank=True, null=True, default=None)
    bg_height = models.IntegerField(editable=False, blank=True, null=True, default=None)
    
    bg_track = models.FileField(upload_to='episode_bgt', 
                                    verbose_name='Musique de fond', 
                                    max_length=255,
                                    blank=True, null=True, default=None);
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Episode, self).save(force_insert, force_update) 
        
    def __unicode__(self):
        return self.title
        
        

def atw_create_profile(sender, **kwargs):
    user = kwargs['instance']
    try:
        UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        p = UserProfile()
        p.user = kwargs['instance']
        p.save()
    else:
        pass
        
def atw_notice_profile(sender, **kwargs):
    from django.core.mail import mail_admins
    profile = kwargs['instance']
    message = [u'Profile update %s <%s>'%(profile.user.get_full_name(), profile.user.email),]
    for attr in [u'title',u'age', u'skills', u'interests', u'city', u'country', u'languages']:
        message.append('%s:'%(attr,))
        try:
            message.append(getattr(profile, attr))
        except Exception:
            pass
            
    try:
        mail_admins('Profile update', '\n\n'.join(message))
    except Exception:
        print('Unable to send profile update notice')
    
        
    
    
models.signals.post_save.connect(atw_create_profile, sender=User, weak=False)
models.signals.post_save.connect(atw_notice_profile, sender=UserProfile, weak=False)
