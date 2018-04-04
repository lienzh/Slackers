#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
import stock.views as views

app_name = 'stock'
urlpatterns = [
				url(r'^$', views.Index.as_view(), name='index'),
				url(r'^device/detail/(?P<pk>\d+)/$', views.DeviceDetail.as_view(), name='device_detail'),
				url(r'^search/', views.DeviceSearch.as_view(), name='device_search'),
				url(r'^about/', views.about, name='about'),
				url(r'^upload$', views.uploadfile, name='device_uploadfile'),
				url(r'^upload2$', views.uploadfile2, name='device_uploadfile2'),
				url(r'^filesys/', views.FileSys.as_view(), name='filesys'),
				#url(r'^download/$', 'views.downloadfile', name = "device_downloadfile"),
				#url(r'^statistics/', views.statistics, name='statistics'),
				#url(r'^login/', views.user_login, name='user_login'),
				#url(r'^logout/', views.user_logout, name='user_logout'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
