from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.user.is_authenticated: 
        return HttpResponseRedirect('/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    if 'next' in request.GET:
        next = str(request.GET['next'])
    else:
        next = "/"
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(next)
    else:
        return render(request, 'login.html', {'next': next})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def ajax_test(request):
    return render(request, 'ajax_test.html')

@csrf_exempt
def ajax_test_add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))
