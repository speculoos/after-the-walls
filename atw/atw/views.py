# -*- coding: utf-8 -*-
"""
atw.views
"""

from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseServerError, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core import serializers
from django.template import RequestContext
from django.shortcuts import get_object_or_404
import json

class HomePageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        return super(HomePageView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        session = self.request.session
        context['session'] = session
        if self.request.user.is_authenticated():
            context['user'] = self.request.user.username
            try:
                context['user_pk'] = self.request.user.id
            except Exception:
                pass
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
            data = { 
            'user':user.username,
            'user_pk':user.id
            }
            
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
    
@csrf_protect
def register_step_0(request):
    name = request.POST.get('name', None)
    email = request.POST.get('email', None)
    from django.contrib import auth
    
    email = auth.models.User.objects.normalize_email(email)
    u = auth.get_user_model()()
    names = name.split(' ')
    firstname = names.pop(0)
    lastname = ' '.join(names)
    try:
        u.username = u.email = email
        u.first_name = firstname
        u.last_name = lastname
        u.is_active = False
        u.save()
        ctx = RequestContext(request)
        w_email = render_to_string('email_reg1.html', {'user':u}, ctx)
        print w_email
        u.email_user('After The Walls Registration', w_email)
    except Exception as e:
        return HttpResponseServerError(json.dumps({'error':str(e)}), mimetype="application/json")
        
    u_data = serializers.serialize("json", [u], fields=('email','first_name','last_name','username'))
    data = json.loads(u_data)[0]
    return HttpResponse(json.dumps(data), mimetype="application/json")
    

def register_step_1(request):
    uname = request.GET.get('user', None)
    key = request.GET.get('key', None)
    print('RS1 (%s) (%s)'%(uname,key))
    from django.contrib import auth
    from django.contrib.contenttypes.models import ContentType
    from utopia.models import Message
    
    u = get_object_or_404(auth.get_user_model(), username=uname)
    if key != u.api_key.key:
        return HttpResponseForbidden('Wrong API_KEY')
    
    content_type = ContentType.objects.get_for_model(Message)
    permission = auth.models.Permission.objects.get(content_type=content_type, codename='add_message')
    a_password = auth.models.User.objects.make_random_password()
    
    u.set_password(a_password)
    u.is_active = True
    u.user_permissions.add(permission)
    u.save()
    
    ctx = RequestContext(request)
    w_email = render_to_string('email_welcome.html', {'user':u, 'password':a_password}, ctx)
    print w_email
    u.email_user('After The Walls Registration', w_email)
    user = auth.authenticate(username=u.get_username(), password=a_password)
    auth.login(request, user)
    
    return HttpResponseRedirect('/')
    
    