# -*- coding: utf-8 -*-
"""
atw.views
"""

from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
import json

class HomePageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        return super(HomePageView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        session = self.request.session
        #if session.get('salt') is None:
            #import uuid
            #session.['salt'] = str(uuid.uuid4())
        context['session'] = session
        
        if self.request.user.is_authenticated():
            context['user'] = self.request.user.username
            try:
                context['key'] = self.request.user.api_key.key
            except Exception:
                pass
        return context
        
        
@csrf_protect
def login(request):
    u = request.POST.get('user', None)
    k = request.POST.get('key', None)
    
    if not u or not k:
        return HttpResponseBadRequest(json.dumps({'error': 'Must provide user and key'}), mimetype="application/json")
        
    from django.contrib import auth
    user = auth.authenticate(username=u, password=k)
    if user is not None and user.is_active:
            auth.login(request, user)
            data = { 'user':user.username, }
            
            try:
                data['api_key'] = user.api_key.key
            except Exception:
                data['api_key'] = 'N'*16
                
            return HttpResponse(json.dumps(data), mimetype="application/json")
    
    return HttpResponseForbidden(json.dumps({'error': 'wrong credentials'}), mimetype="application/json")
    
@csrf_protect
def logout(request):
    from django.contrib import auth
    request.session.flush()
    auth.logout(request)
    return HttpResponse(json.dumps({'logout':'success'}), mimetype="application/json")
    
