# -*- coding: utf-8 -*-
"""
utopia.models
"""

from django.db import models
from django.template.defaultfilters import slugify

from adminsortable.models import Sortable

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
    episode = models.ForeignKey('Episode', verbose_name='Épisode', blank=True, null=True, default=None)
    
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
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Episode, self).save(force_insert, force_update) 
        
    def __unicode__(self):
        return self.title
        