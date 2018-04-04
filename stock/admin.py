# coding: utf-8
from django.contrib import admin
from .models import Inventory,Device

# Register your models here.
#admin.site.register(Device)
admin.site.register(Inventory)


class DeviceAdmin(admin.ModelAdmin): #这个是为了美观，防止意外，也可以不要
	readonly_fields = ('devthumb',) #因为不需要在后台修改该项，所以设置为只读
	def get_readonly_fields(self, request, obj=None):
		if obj: #editing an existing object
			return self.readonly_fields
		return self.readonly_fields

admin.site.register(Device, DeviceAdmin)
