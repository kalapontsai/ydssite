from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
import csv
import os,sys
from datetime import datetime
from django.conf import settings
import logging

def bom(request):
	#if not request.user.is_authenticated:
		#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	#if not request.user.has_perm('ate.view_testdata'):
		#return HttpResponseRedirect('/unauthorized/')
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	myDate = datetime.now()
	log_date = str(myDate.strftime("%Y/%m/%d %H:%M:%S"))
	logger.info('%s visit %s at %s' % (ip,request.path,log_date))
	filename = 'TIPTOP-ALL.csv'
	f = os.path.join(settings.STATICFILES_DIRS[3][1],filename).replace('\\','/')
	csvfile = open(f, newline='')
	rows = csv.reader(csvfile)
	# 以迴圈輸出每一列 arr.append({'date':dt, 'lotname':
	cp = []
	rs = []
	co = []
	bo = []
	ms = []
	xf = []
	di = []
	ic = []
	pc = []
	ls = []
	tr = []
	for row in rows:
		if row[0][2:4] == 'CP' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			cp.append({'content':tmp_txt})
		if row[0][2:4] == 'RS' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			rs.append({'content':tmp_txt})
		if row[0][2:4] == 'CO' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			co.append({'content':tmp_txt})
		if row[0][2:4] == 'BO' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			bo.append({'content':tmp_txt})
		if row[0][2:4] == 'MS' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			ms.append({'content':tmp_txt})
		if row[0][2:4] == 'XF' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			xf.append({'content':tmp_txt})
		if row[0][2:4] == 'DI' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			di.append({'content':tmp_txt})
		if row[0][2:4] == 'IC' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			ic.append({'content':tmp_txt})
		if row[0][2:4] == 'PC' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			pc.append({'content':tmp_txt})
		if row[0][2:4] == 'LS' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			ls.append({'content':tmp_txt})
		if row[0][2:4] == 'TR' :
			tmp_txt = row[2] + '--' + row[1] + '--' + row[0]
			tr.append({'content':tmp_txt})
	csvfile.close()

	return render(request, 'rd_bom.html', {'cp':cp,'rs':rs, 'co':co, 'bo':bo,\
		'ms':ms, 'xf':xf, 'di':di,'ic':ic, 'pc':pc, 'ls':ls,'tr':tr})

def bom1(request):
	#if not request.user.is_authenticated:
		#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	#if not request.user.has_perm('ate.view_testdata'):
		#return HttpResponseRedirect('/unauthorized/')
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	myDate = datetime.now()
	log_date = str(myDate.strftime("%Y/%m/%d %H:%M:%S"))
	logger.info('%s visit %s at %s' % (ip,request.path,log_date))
	
	filename = 'TIPTOP-ALL.csv'
	f = os.path.join(settings.STATICFILES_DIRS[3][1],filename).replace('\\','/')
	csvfile = open(f, newline='')
	rows = csv.reader(csvfile)
	
	# 以迴圈輸出每一列 arr.append({'date':dt, 'lotname':
	comp_type = ['CP','RS','CO','BO','MS','XF','DI','IC','PC','LS','TR']
	comp_list = []
	for row in rows:
		if row[0][2:4] in comp_type:
			tmp_txt = row[1] + '--' + row[2] + '--' + row[0]
			comp_list.append({'type':row[0][2:4] , 'content':tmp_txt})
	csvfile.close()
#讀取PCB輸出檔
	pcb_list = []
	path = ""
	
	if 'txt_path' in request.POST :
		path = str(request.POST['txt_path'])
		if os.path.isfile(path):
			try:
				csvfile = open(path, newline='')
				rows = csv.reader(csvfile)
				idx = 0
				for row in rows:
					pcb_list.append({'pos':row[1],'spec':row[0],'idx':idx})
					idx += 1
			except:
				pcb_list.append({'pos':"讀取異常,請檢查檔案格式",'spec':"na",'idx':"0"})
		else:
			pcb_list.append({'pos':"路徑或檔名錯誤",'spec':"na",'idx':"0"})
	if len(pcb_list) < 1 :
		pcb_list.append({'pos':"na",'spec':"na",'idx':"0"})

	return render(request, 'rd_bom2.html', {'path':path, 'pcb_list':pcb_list, 'comp_list':comp_list})
