from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.admin.widgets import AdminDateWidget
import csv
import os,sys,time
from django.conf import settings

def cal(request):
	if request.POST:
		badge = str(request.POST['badge'])
		yourdate = str(request.POST['date1'])
		issuer = str(request.POST['issuer'])
		return render(request, 'cal1.html', {'issuer':issuer, 'yourdate': yourdate, 'badge':badge})
	else:
		return render(request, 'cal1.html')
	
	#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	return render(request, 'cal1.html')

def board(request):
	#uploads = os.path.join(STATIC_ROOT,'uploads').replace('\\','/')
	filename = 'hr_board.csv'
	#f = os.path.join(uploads,filename)
	#csvfile = open(f, newline='')
	#rows = csv.reader(csvfile)

	# 以迴圈輸出每一列
	#tmp = []
	#for row in rows:
		#tmp.append(row)
	#csvfile.close()

	#lotname = tmp[4][0][4:]
	#device = tmp[1][0][41:]

	return render(request, 'hr_board.html', {'tmp':'111'})