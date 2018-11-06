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
from ydssite import yds_db_config_default as yds
import cx_Oracle
import logging

configs = yds.oracle_db
user = configs['db']['user']
host = configs['db']['host']
pwd = configs['db']['pwd']

@csrf_exempt
def stock_query_ajax(request):
	a = str(request.GET['a'])
	connection = cx_Oracle.connect(user, pwd, host)
	cursor = connection.cursor()
	sql = "select img01,sum(img10) from yuandean1.img_file where img23='Y' and img10<>0 and img01='" + a + "' group by img01 order by 1"
	# 10CP00001N-0002 , 10BS060000-0002
	cursor.execute(sql)
	result = []
	for i in cursor:
			result.append({'field1':i[0],'field2':i[1]})
	if len(result) == 0:
		result.append({'field1':a,'field2':'0'})

	connection.close()
	return HttpResponse(result)

def stock_query(request):
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))
	#模糊搜尋
	#select img01,sum(img10) from yuandean1.img_file where img23='Y' and img10<>0 and img01 like '10BS060000-0002%' group by img01 order by 1;
	if 'pn' in request.POST :
		pn = str(request.POST['pn']).upper()
		connection = cx_Oracle.connect(user, pwd, host)
		cursor = connection.cursor()
		#單位 = img09
		sql = "select img01,sum(img10) from yuandean1.img_file where ROWNUM < 1000 and img23='Y' and img10<>0 and img01 like '" + pn + "' group by img01 order by 1"
		cursor.execute(sql)
		#logger.debug(sql)
		result = []
		#accnt = 0
		for i in cursor:
			result.append({'pn':i[0],'qty':i[1]})
			#accnt += 1
		#logger.debug("acc=%s" % accnt)
		connection.close()
		return render(request, 'stock_query.html',{'result':result})
	return render(request, 'stock_query.html')

def bom(request):
	#if not request.user.is_authenticated:
		#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	#if not request.user.has_perm('ate.view_testdata'):
		#return HttpResponseRedirect('/unauthorized/')
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))
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
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))
#讀取PCB輸出檔
#20181101 欄位變更為 row[0]:零件位置 row[1]:規格
	pcb_list = []
	path = ""
	err = 0
	if 'txt_path' in request.POST :
		path = str(request.POST['txt_path'])
		if os.path.isfile(path):
			try:
				csvfile = open(path, newline='')
				rows = csv.reader(csvfile)
				idx = 0
				for row in rows:
					if row[1] == "": #若規格空白則補值
						t_spec = "na"
					else:
						t_spec = row[1]
					pcb_list.append({'pos':row[0],'spec':t_spec,'idx':idx})
					idx += 1
				logger.info("CSV load:%s" % (path))
			except:
				logger.error("讀取異常:%s" % (path))
				pcb_list.append({'pos':"讀取異常,請檢查檔案格式",'spec':"na",'idx':"0"})
				err = 1
		else:
			logger.error("路徑或檔名錯誤:%s" % (path))
			pcb_list.append({'pos':"路徑或檔名錯誤",'spec':"na",'idx':"0"})
			err = 1
#讀取 bom p/n,spec,庫存數
		if err == 0:
			connection = cx_Oracle.connect(user, pwd, host)
			cursor = connection.cursor()
			filename = 'TIPTOP-ALL.csv'
			f = os.path.join(settings.STATICFILES_DIRS[3][1],filename).replace('\\','/')
			csvfile = open(f, newline='')
			rows = csv.reader(csvfile)
			
			# 以迴圈輸出每一列 arr.append({'date':dt, 'lotname':
			comp_type = ['CP','RS','CO','BO','MS','XF','DI','IC','PC','LS','TR']
			comp_list = []
			sql=""
			for row in rows:
				if row[0][2:4] in comp_type:
					#取tiptop庫存數
					com_qty = "0"
					sql = "select img01,sum(img10) from yuandean1.img_file where img23='Y' and img10<>0 and img01='" + row[0] + "' group by img01 order by 1"
					cursor.execute(sql)
					for i in cursor:
						com_qty = str(i[1])

					tmp_txt = row[1] + '--' + row[2] + '--' + row[0] + '--' + com_qty
					comp_list.append({'type':row[0][2:4] , 'content':tmp_txt})
			csvfile.close()
			connection.close()
			return render(request, 'rd_bom1.html', {'path':path, 'pcb_list':pcb_list, 'comp_list':comp_list})
	if len(pcb_list) < 1:
		pcb_list.append({'pos':"na",'spec':"na",'idx':"0"})
	return render(request, 'rd_bom1.html', {'path':path, 'pcb_list':pcb_list})
	
