# -*- coding: utf-8 -*-
"""
utopia.models
"""

from django.db import models
from django.template.defaultfilters import slugify


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
        