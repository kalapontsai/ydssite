from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django import template
from .models import Lottitle,Testdata,Testresult,Testunit

def index(request):
    return render(request, 'ateindex.html')

def test_item_list(request):
	t_item = Testunit.objects.all().order_by('col')
	return render(request, 'ate_test_item_list.html', {'raw': t_item})

def device_yield(request):
	#distinct = Lottitle.objects.values('device').annotate(device_count=Count('device')).filter(device_count=1)
	#t_row = User.objects.filter(device__in=[item['device'] for item in distinct])
	devices = []
	rows = Lottitle.objects.values('device').distinct()
	### 把queryset轉成list ###
	for de in rows:
		devices.append(de['device']) #device[0]['device']

	if 'device' in request.POST:
		device = str(request.POST['device'])
	else:
		device = devices[0]

	yield_array = []
	lots = Lottitle.objects.values('lotdt_idx').filter(device=device)
	for lot in lots :
		tmp_yields = Testdata.objects.values('t_result').filter(lotdt_idx=lot['lotdt_idx'])
		total = 0
		good = 0
		for tmp_yield in tmp_yields :
			total += 1
			if tmp_yield['t_result'] == 1 :
				good += 1
		yield_cal = round (good * 100 / total , 2)
		yield_array.append([device,lot['lotdt_idx'],total,good,yield_cal])



	return render(request, 'device_yield.html', {'devices': devices, 'lots':yield_array})
