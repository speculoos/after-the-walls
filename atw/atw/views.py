# -*- coding: utf-8 -*-
"""
atw.views
"""

from django.views.generic.base import TemplateView
from django.http import 

class HomePageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        return super(HomePageView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['session'] = self.request.session
            context['user'] = self.request.user.username
            context['key'] = self.request.user.api_key.key
        return context
        
        

def login(request):
    u = request.POST.get('user', None)
    k = request.POST.get('key', None)
    if not u or not k:
        return HttpResponseBadRequest('Must provide user and key')
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate, login
    