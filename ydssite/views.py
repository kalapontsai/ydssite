from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User,Group
from datetime import datetime
import json
#from django.core.mail import EmailMessage

def visit_account(str = 'na'):
    with open('count.json') as f:
        data = json.load(f)
    
    if (str == 'na'):
        data['visit'] += 1
    else :
        data['page'][str] += 1

    with open('count.json','w') as f:
        json.dump(data, f)

    return

def index(request):
    #列出某group中有哪些人
    #qs = User.objects.filter(groups__name__in=['RD1'])
    #列出使用者的群組名單
    #qry = Group.objects.filter(user = request.user)
    #<QuerySet [<Group: RD1>, <Group: HR>, <Group: users>]>
    ip = request.META['REMOTE_ADDR']
    if 'visited' not in request.session:
        visit_account()
        request.session['visited'] = '1'
    request.session.set_expiry(3600)
    #request.session.session_key
    a = request.session.get_expiry_age()
    return render(request, 'index.html',{'ss':a})

def unauthorized(request):
    return render(request, 'unauthorized.html')

def login(request):
    if request.user.is_authenticated: 
        return HttpResponseRedirect('/')
    if 'next' in request.GET:
        next = str(request.GET['next'])
    else:
        next = "/"
    if 'username' in request.POST:
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next)
    return render(request, 'login.html', {'next': next})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def ajax_test(request):
    #email = EmailMessage('Hello', 'Body goes here.', 'from@example', ['to@example.com', 'to2@example.com'], ['bcc@example.com'])
    #email = EmailMessage('Hello', 'Body goes here.', 'Test', ['ben_tsai@yds.com.tw'], )
    #email.send()
    return render(request, 'ajax_test.html')

@csrf_exempt
def ajax_test_add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))
