from __future__ import unicode_literals
import math
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django import template
from .models import Lottitle,Testdata,Testresult,Testunit

def index(request):
	#'ateindex.html'
    return render(request, 'ateindex.html')

def test_item_list(request):
	t_item = Testunit.objects.all().order_by('col')
	return render(request, 'ate_test_item_list.html', {'raw': t_item})

def device_yield(request):
	devices = []
	rows = Lottitle.objects.values('device').distinct()
	### 把queryset轉成list ###
	for de in rows:
		devices.append(de['device']) #device[0]['device']

	if 'device' in request.POST:
		device = str(request.POST['device'])
	else:
		device = devices[0]

	arr = []
	lots = Lottitle.objects.values('lotdt_idx','lotname').filter(device=device)
	for lot in lots :
		tmp_yields = Testdata.objects.values('t_result').filter(lotdt_idx=lot['lotdt_idx'])
		total = 0
		good = 0
		for tmp_yield in tmp_yields :
			total += 1
			if tmp_yield['t_result'] == 1 :
				good += 1
		yield_cal = round (good * 100 / total , 2)
		dt = str(lot['lotdt_idx'])[:5] + '/' + str(lot['lotdt_idx'])[4:6] + '/' + str(lot['lotdt_idx'])[6:8]
		#data = { 'lotname':lot['lotname'],'total':total, 'good':good, 'yield_cal':yield_cal}
		arr.append({'date':dt, 'lotname':lot['lotname'],'total':total, 'good':good, 'yield_cal':yield_cal})



	return render(request, 'device_yield.html', {'devices': devices,'device': device, 'arr':arr})

def spcc_xr(request):
	#列出測項清單
	test_items = Testunit.objects.values('col','unit','name').order_by('col')
	if 'col' in request.POST:
		col = int(request.POST['col'])
	else:
		col = 1
	for i in test_items:
		if i['col'] == col :
			test_item = i['name']
			t_unit = i['unit']
	#列出機種名稱
	devices = []
	rows = Lottitle.objects.values('device').distinct()
	### 把queryset轉成list ###
	for de in rows:
		devices.append(de['device'])
	if 'device' in request.POST:
		device = str(request.POST['device'])
	else:
		device = devices[0]

	#列出lot id
	item_no = "col_" + str(col)
	t_item_h = item_no + "_h"
	t_item_l = item_no + "_l"
	rows = Lottitle.objects.values('lotdt_idx','lotname',t_item_h,t_item_l)\
	.order_by('lotdt_idx').filter(device=device)
	limit = 10
	sample_lot = 0
	sample_pcs = 0
	lots = []
	top_all = [] #所有的值
	rang_r = 0
	for t_lot in rows:
		if sample_lot >= limit:
			break
		top5_data = Testdata.objects.values(item_no).filter(lotdt_idx=t_lot['lotdt_idx'],\
			t_result=1)[:5]
		top_5 = []
		sum_num = 0
		for tt in top5_data:
			top_5.append(tt[item_no])
			top_all.append(tt[item_no])
			sum_num += tt[item_no]
			sample_pcs += 1
		if len(top_5) < 1:
			continue
			#top_5 = [0,0,0,0,0]
		max_num = max(top_5)
		min_num = min(top_5)
		rang_num = round(max_num - min_num,3)
		avg_num = round(sum_num/len(top_5),3)
		lot_dt = str(t_lot['lotdt_idx'])[:8]


		lots.append({'lotdt':lot_dt, 'lotname':t_lot['lotname'],'col_h':t_lot[t_item_h],\
			'col_l':t_lot[t_item_l],'top5':top_5,'avg_num':avg_num,'rang_num':rang_num})
		rang_r += rang_num
		sample_lot += 1
	x_bar = round(sum(top_all)/len(top_all),3)
	r_bar = round(rang_r/sample_lot,3)
	#檢查是否為有效值
	if x_bar != 0 and r_bar != 0:
		#標準差
		sigma_x = 0
		for i in top_all:
			sigma_x += pow(i-x_bar,2)
		std_dev = round(math.sqrt(sigma_x/(len(top_all)-1)),3)

		#管制上下限
		#管制圖係數 樣本數,A2,D3,D4
		stastics_table = [[2,1.88,0,3.267],[3,1.023,0,2.575],[4,0.729,0,2.282],[5,0.577,0,2.115],\
		[6,0.483,0,2.004],[7,0.419,0.076,1.924],[8,0.373,0.136,1.864],[9,0.337,0.184,1.816],[10,0.308,0.223,1.777]]
		A2 = 0
		for a in stastics_table:
			if a[0] == 5: #暫固定抽樣數為5
				A2 = a[1]
				D3 = a[2]
				D4 = a[3]
		if A2 == 0:
			A2 = 0.577

		UCL = round(x_bar + A2 * r_bar,3)
		LCL = round(x_bar - A2 * r_bar,3)
		Cp = round((t_lot[t_item_h] - t_lot[t_item_l] ) / (6 * std_dev),2)
		Cpu = round(abs(t_lot[t_item_h] - x_bar ) / (3 * std_dev),2)
		Cpl = round(abs(t_lot[t_item_l] - x_bar ) / (3 * std_dev),2)
		Cpk = min([Cpu,Cpl])

		spc = {'device':device,'test_item':test_item,'col':col, 'unit': t_unit,'x_bar':x_bar,\
		'r_bar':r_bar,'sample_pcs':len(top_all),'std_dev':std_dev,'UCL':UCL,'LCL':LCL,'Cp':Cp,\
		'Cpk':Cpk,'USL':t_lot[t_item_h],'LSL':t_lot[t_item_l]}
	else:
		spc = {'device':device,'test_item':test_item,'col':col, 'unit': t_unit,'x_bar':0,\
		'r_bar':0,'sample_pcs':len(top_all),'std_dev':0,'UCL':0,'LCL':0,'Cp':0,\
		'Cpk':0,'USL':t_lot[t_item_h],'LSL':t_lot[t_item_l]}

	return render(request, 'spcc_xr.html', {'test_items': test_items, 'devices': devices,'lots': lots,'spc':spc})