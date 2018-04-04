#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from .models import Device,Inventory
from stock.forms import SearchForm,UploadFileForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response
from django.template import RequestContext
import xlrd
from django.http import HttpResponseRedirect
# Create your views here.

class Index(TemplateView):
	template_name = 'stock/index.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['searchForm'] = SearchForm()
		return context

class DeviceSearch(ListView):
	template_name = 'stock/search.html'
	context_object_name = 'device'	

	def get_queryset(self, **kwargs):
		search_by = self.request.GET.get('search_by', '描述')
		current_path = self.request.get_full_path()
		keyword = self.request.GET.get('keyword', u'_所有备件')
		if keyword == u'_所有备件':
			queryset = Device.objects.all()
		else:
			keyword = self.request.GET.get('keyword', None)
			if search_by == u'描述':
				queryset = Device.objects.filter(description__contains=keyword).order_by('-ERP')[0:1000]
			elif search_by == u'ERP':
				queryset = Device.objects.filter(ERP__contains=keyword).order_by('-ERP')[0:1000]
			elif search_by == u'使用方向':
				queryset = Device.objects.filter(usepart__contains=keyword).order_by('-ERP')[0:1000]

		for que in queryset:
			que.quotanum = 0
			for inve in que.inventory_set.all():
				que.quotanum += inve.quantity
			

		paginator = Paginator(queryset, 5)
		page = self.request.GET.get('page', 1)

		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			queryset = paginator.page(1)
		except EmptyPage:
			queryset = paginator.page(paginator.num_pages)
    	# ugly solution for &page=2&page=3&page=4
		if '&page' in current_path:
			current_path = current_path.split('&page')[0]
		return queryset


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		search_by = self.request.GET.get('search_by', '描述')
		current_path = self.request.get_full_path()
		keyword = self.request.GET.get('keyword', u'_所有备件')
		context.update({
			'search_by': search_by,
			'keyword': keyword,
			'current_path': current_path,
			'searchForm': SearchForm(),
		})
		return context

class DeviceDetail(DetailView):
	template_name = 'stock/device_detail.html'
	model = Device
	context_object_name = 'device'
	pk_url_kwarg = 'pk'

	def get_context_data(self, **kwargs):
		inventory_list = self.object.inventory_set.all()
		context = super().get_context_data(**kwargs)
		context['inventory_list'] = inventory_list
		return context

class FileSys(TemplateView):
    template_name = 'stock/filesys.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def about(request):
    return render(request, 'stock/about.html', {})

def uploadfile(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		#if form.is_valid():
		with open('media/file/1.xls', 'wb+') as destination:
			for chunk in request.FILES['input-44'].chunks():
				destination.write(chunk)
		#fd = open('media/file/1.xls')
		wb = xlrd.open_workbook('media/file/1.xls')
		table = wb.sheets()[0]
		row = table.nrows
		for i in range(row):
			ERP = table.row_values(i)[0]
			description = table.row_values(i)[1]
			#quota = table.row_values(i)[2]
			#quotanum = table.row_values(i)[3]
			unit = table.row_values(i)[4]
			price = table.row_values(i)[5]
			#devimg = table.row_values(i)[6]
			#devclass = table.row_values(i)[7]
			#usesys = table.row_values(i)[8]
			#usepart = table.row_values(i)[9]
			#ERP,description,quota,quotanum,unit,price,devimg,devclass,usesys,usepart = line.split('\'')
			#Device.objects.get_or_create(ERP=ERP, description=description, quota=quota, quotanum=quotanum, unit=unit, price=price, devimg=devimg, devclass=devclass, usesys=usesys, usepart=usepart)
			Device.objects.get_or_create(ERP=ERP, description=description, unit=unit, price=price)
		#fd.close()
		return HttpResponseRedirect('/about/')
        #return render_to_response('stock/success.html', {'form': form, })
        #return render_to_response('stock/success.html')
        #return render(request, 'stock/success.html', {})
	else:
		form = UploadFileForm()
		#return render_to_response('stock/upload.html', {'form': form, }, context_instance=RequestContext(request))
	return render_to_response('stock/success.html', {'form': form, })

def uploadfile2(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		with open('media/file/2.xls', 'wb+') as destination:
			for chunk in request.FILES['input-45'].chunks():
				destination.write(chunk)
		#wb = xlrd.open_workbook(filename=None, file_contents=request.FILES['input-45'].read()) # 关键点在于这里
		wb = xlrd.open_workbook('media/file/2.xls')
		table = wb.sheets()[0]
		row = table.nrows
		#fd = open('media/file/2.txt')
		#for line in fd:
		for i in range(row):
			#col = table.row_values(i)
			ERP = table.row_values(i)[0]
			description = table.row_values(i)[1]
			location = table.row_values(i)[2]
			quantity = table.row_values(i)[3]
#			ERP, description, location, quantity = line.split('\'')
			for d in Device.objects.all():
				if d.ERP == ERP:
					Inventory.objects.get_or_create(ERP=d, description=description, location=location, quantity=quantity)
					break;

		#return HttpResponseRedirect('/about/')
		#return render_to_response('stock/success.html', {'form': form, })
		#return render_to_response('stock/success.html')
		#return render(request, 'stock/success.html', {})
	else:
		form = UploadFileForm()
		#return render_to_response('stock/upload.html', {'form': form, }, context_instance=RequestContext(request))
	return render_to_response('stock/success.html', {'form': form, })

