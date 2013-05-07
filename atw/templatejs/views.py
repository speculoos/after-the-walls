# -*- coding: utf-8 -*-
"""
templatejs.views

The idea here is to forward templates to underscore
benefits:
 - Django i18n

"""

from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.generic import TemplateView 

class TemplateJSView(TemplateView):
    def get_template_names(self):
        if 'template_name' not in self.kwargs:
            return HttpResponseBadRequest('You MUST provide a template name')
        return [self.kwargs['template_name']]
    
