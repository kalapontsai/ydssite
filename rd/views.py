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

def bom1(request):
	filename = 'TIPTOP-ALL.csv'
	log_
	f = os.path.join(settings.STATICFILES_DIRS[3][1],filename).replace('\\','/')
	csvfile = open(f, newline='')
	rows = csv.reader(csvfile)
	# 以迴圈輸出每一列 arr.append({'date':dt, 'lotname':
	p_type = ['cp','rs','co','bo','ms','xf','di','ic','pc','ls','tr']
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

	return render(request, 'rd_bom1.html', {'cp':cp,'rs':rs, 'co':co, 'bo':bo,\
		'ms':ms, 'xf':xf, 'di':di,'ic':ic, 'pc':pc, 'ls':ls,'tr':tr})

def bom(request):
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
