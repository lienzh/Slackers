#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse
from PIL import Image
import os
from Lestock.settings import MEDIA_ROOT, THUMB_ROOT
from django.db.models.fields.files import ImageFieldFile

# Create your models here.


# 缩略图的生成
# 以size为宽，等比例缩放
def make_thumb(spath, size = 480):
	pixbuf = Image.open(spath)
	width, height = pixbuf.size

	if width > size:
		delta = width / size
		height = int(height / delta)
		pixbuf.thumbnail((size, height), Image.ANTIALIAS)
		return pixbuf

# 设备清单
class Device(models.Model):
	ERP = models.CharField(max_length=15, primary_key=True)
	description = models.CharField(max_length=128)
	quota = models.CharField(max_length=15, blank=True)
	quotanum = models.IntegerField(default=0)
	unit = models.CharField(max_length=4, default=u"个")
	price = models.FloatField(null=True)
	devimg = models.ImageField(upload_to = 'screenshots',blank=True,default='screenshots/default.jpg')
	devimg1 = models.ImageField(upload_to = 'screenshots',blank=True,default='screenshots/default.jpg')
	devimg2 = models.ImageField(upload_to = 'screenshots',blank=True,default='screenshots/default.jpg')
	devthumb = models.ImageField(upload_to = 'thumb',blank=True,default='thumb/default.jpg')
	#devthumb1 = models.ImageField(upload_to = 'thumb',blank=True,default='thumb/default.jpg')
	#devthumb2 = models.ImageField(upload_to = 'thumb',blank=True,default='thumb/default.jpg')
	devclass = models.CharField(max_length=15, blank=True)
	usesys = models.CharField(max_length=15, blank=True)
	usepart = models.CharField(max_length=15, blank=True)
	def save(self):
		super(Device, self).save() #将上传的图片先保存一下，否则报错
		base, ext = os.path.splitext(os.path.basename(self.devimg.path))
		if base != 'default':
			thumb_pixbuf = make_thumb(os.path.join(MEDIA_ROOT, self.devimg.name))
			relate_thumb_path = os.path.join(THUMB_ROOT, base + '.thumb' + ext)
			thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
			thumb_pixbuf.save(thumb_path)
			thumb_path1 = 'thumb/'+base+'.thumb'+ext
			self.devthumb = ImageFieldFile(self, self.devthumb, thumb_path1)
		super(Device, self).save() #再保存一下，包括缩略图等
	def __str__(self):
		return self.description
	def get_absolute_url(self):
		return reverse('stock:device_detail', kwargs={'pk': self.pk})

# 库存清单
class Inventory(models.Model):
	ERP = models.ForeignKey(Device,blank=True)
	description = models.CharField(max_length=128)
	location = models.CharField(max_length=15, default=u"ERP库")
	quantity = models.IntegerField(default=0)
	def __str__(self):
		return self.description
