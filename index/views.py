from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django import template

def index(request):
    return render(request, 'index.html')