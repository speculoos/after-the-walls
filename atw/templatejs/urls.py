from django.conf.urls import patterns, include, url

from templatejs.views import TemplateJSView

urlpatterns = patterns('',
    url(r'^(?P<template_name>.+)$', TemplateJSView.as_view(), name='template'),
)
