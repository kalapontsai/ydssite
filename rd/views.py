#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.conf import settings
import csv
import os,sys
from ydssite import yds_db_config_default as yds
import cx_Oracle
import logging
import json

configs = yds.oracle_db
user = configs['db']['user']
host = configs['db']['host']
pwd = configs['db']['pwd']

def stock_query(request):
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))
	#模糊搜尋
	#select img01,sum(img10) from yuandean1.img_file where img23='Y' and img10<>0 and img01 like '10BS060000-0002%' group by img01 order by 1;
	qry_txt = ["","","","",""]
	if 'qry_bom' in request.POST :
		qry_bom = str(request.POST['qry_bom']).upper()
		qry_pn = str(request.POST['qry_pn'])
		qry_spec = str(request.POST['qry_spec'])
		qry_fox = str(request.POST['qry_fox']).upper()
		if request.POST['qry_stock'].isnumeric():
			qry_stock = str(request.POST['qry_stock'])
		else:
			qry_stock = "0"
		qry_txt = [qry_bom,qry_pn,qry_spec,qry_fox,qry_stock]
		if qry_bom == "" and qry_pn == "" and qry_spec == "" and qry_fox == "":
			return render(request, 'stock_query.html')
		
		connection = cx_Oracle.connect(user, pwd, host)
		cursor = connection.cursor()
		#ima01=料號,ima02=單位 = img09
		#sql = "select img01,sum(img10) from yuandean1.img_file where ROWNUM < 1000 and img23='Y' and img10<>0 and img01 like '" + pn + "' group by img01 order by 1"
		sql = "select if1.ima01,if1.ima02,if1.ima021,if1.ima25,if1.ima916,if1.imaud03,NVL(gf1.g10,0) from yuandean1.ima_file if1 left outer join (select img01 g1,sum(img10) g10 from yuandean1.img_file where img23='Y' group by img01) gf1 on (if1.ima01=gf1.g1) where ROWNUM < 1000"
		sql_qry = ""
		if qry_bom != "":
			sql_qry += "and if1.ima01 like '%" + qry_bom + "%' "
		if qry_pn != "":
			sql_qry += "and if1.ima02 like '%" + qry_pn + "%' "
		if qry_spec != "":
			sql_qry += "and if1.ima021 like '%" + qry_spec + "%' "
		if qry_fox != "":
			sql_qry += "and if1.imaud03 like '%" + qry_fox + "%' "
		sql_qry += "and NVL(gf1.g10,0) >= " + qry_stock
		sql += sql_qry + " order by 1"
		cursor.execute(sql)
		#logger.debug(sql)
		result = []
		for i in cursor:
			result.append({'bom':i[0],'pn':i[1],'spec':i[2],'fox':i[5],'stock':i[6]})
			#logger.debug("qry code= %s" % i[1])
		connection.close()
		logger.info('%s' % (ip))
		logger.debug("query = '%s'" % sql_qry)
		return render(request, 'stock_query.html',{'result_stock':result,'qry_txt':qry_txt})
	return render(request, 'stock_query.html',{'qry_txt':qry_txt})

@csrf_exempt
def bom_ajax(request):
	logger = logging.getLogger(__name__)
	comp_type = str(request.GET['comp_type'])
	page = str(request.GET['page'])
	connection = cx_Oracle.connect(user, pwd, host)
	cursor = connection.cursor()
	if page == 'bom':
		sql = "select ima01,convert(ima02||'','UTF8','AL32UTF8') ima02,ima021 from yuandean1.ima_file where"
		sql += " ROWNUM < 1000 and ima01 like '10" + comp_type + "%'"

		#logger.debug("ajax query = '%s'" % sql)
		cursor.execute(sql)
		
		result = []
		for i in cursor:
			result.append({'content':str(i[0]) + "--" + str(i[1]) + "--" + str(i[2])})

	if page == 'bom1':
		sql = "select if1.ima01,if1.ima02,if1.ima021,NVL(gf1.g10,0) from yuandean1.ima_file if1 left outer join (select img01 g1,sum(img10) g10 from yuandean1.img_file where img23='Y' group by img01) gf1 on (if1.ima01=gf1.g1) where"
		sql += " ROWNUM < 1000 and ima01 like '10" + comp_type + "%'"

		#logger.debug("ajax query = '%s'" % sql)
		cursor.execute(sql)
		result = []
		for i in cursor:
			result.append({'content':str(i[1]) + "--" + str(i[2]) + "--" + str(i[0]) + "--" + str(i[3])})

	if len(result) < 1:
		result.append({'content':"無紀錄"})
	connection.close()
	#return HttpResponse(result)
	return HttpResponse(json.dumps(result), content_type="application/json")

def bom(request):
	#if not request.user.is_authenticated:
		#return HttpResponseRedirect('/accounts/login/?next={0}'.format(request.path))
	#if not request.user.has_perm('ate.view_testdata'):
		#return HttpResponseRedirect('/unauthorized/')
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))

	comp_type = ['CP','RS','CO','BO','MS','XF','DI','IC','PC','LS','TR','PB','WI','PN','CS','RV','IS','BS','TA']

	return render(request, 'rd_bom.html', {'comp_type':comp_type})

def bom1(request):
	ip = request.META['REMOTE_ADDR']
	logger = logging.getLogger(__name__)
	logger.info('%s' % (ip))
#讀取PCB輸出檔
#20181101 欄位變更為 row[0]:零件位置 row[1]:規格
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
		else:
			logger.error("路徑或檔名錯誤:%s" % (path))
			pcb_list.append({'pos':"路徑或檔名錯誤",'spec':"na",'idx':"0"})
		csvfile.close()
	#元件庫類別
	comp_type = ['CP','RS','CO','BO','MS','XF','DI','IC','PC','LS','TR','PB','WI','PN','CS','RV','IS','BS','TA']
	if len(pcb_list) < 1:
		pcb_list.append({'pos':"na",'spec':"na",'idx':"0"})
	return render(request, 'rd_bom1.html', {'path':path, 'pcb_list':pcb_list, 'comp_type':comp_type})

def bom1_a(request):
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
	
