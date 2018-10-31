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
from datetime import datetime
from .models import lunch
import pyodbc
from ydssite import ateconfig_default
import logging

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

def lunch_l(request):
	#if not request.user.is_authenticated:
		#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	myDate = datetime.now()
	log_date = str(myDate.strftime("%Y/%m/%d %H:%M:%S"))
	logger.info('%s visit %s at %s' % (ip,request.path,log_date))
	if request.user.has_perm('hr.add_lunch'):
		perms_add = True
	else:
		perms_add = False

	sql = ""
	if 'issue_date' in request.POST:
		configs = ateconfig_default.configs
		driver = configs['db']['driver']
		host = configs['db']['host']
		user = configs['db']['user']
		password = configs['db']['password']
		db = configs['db']['database']

		issue_date = str(request.POST['issue_date'])
		if 'issuer' in request.POST:
			issuer = str(request.POST['issuer'])
		if 'badge' in request.POST:
			badge = str(request.POST['badge'])
		if 'effect_date' in request.POST:
			effect_date = str(request.POST['effect_date'])
		if 'note' in request.POST:
			note = str(request.POST['note'])
		#連接資料庫
		conn = pyodbc.connect('DRIVER='+driver+';SERVER='+host+';DATABASE='+db+';UID='+user+';PWD='+password)
		c = conn.cursor()
		sql = "INSERT INTO hr_lunch (issue_date,issuer,effect_date,badge_list,note)"
		sql += "VALUES ('" + issue_date + "','" + issuer + "','" + effect_date
		sql += "','" + badge + "','" + note + "')"
		c.execute(sql)
		conn.commit()
		conn.close()
	myDate = datetime.now()
    #formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
	issue_date = str(myDate.strftime("%Y/%m/%d %H:%M:%S"))
	formatedmonth = myDate.strftime("%Y-%m")
	formatedday = myDate.strftime("%m-%d")
#    badgelist = badge_list.objects.all().order_by('badge') #還可以加過濾條件.filter(條件式) .filter(effect_date == '2018-08-08' )
	m_list = lunch.objects.all().order_by('-effect_date','issuer').filter(effect_date__contains = formatedmonth)
	

	return render(request, 'lunch_list.html', {'month': formatedmonth, 'tday': formatedday, 'm_list':m_list, 'issuedate':issue_date,'perms_add':perms_add })