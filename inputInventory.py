#!/usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lestock.settings") 

import django
django.setup()

def main():
	from stock.models import Inventory,Device
	f = open('inventoryData.txt')
	for line in f:
		ERP, description, location, quantity = line.split('\'')
		for d in Device.objects.all():
			if d.ERP == ERP:
				Inventory.objects.get_or_create(ERP=d, description=description, location=location, quantity=quantity)
				break;
	f.close()

if __name__ == "__main__":
	main()
	print('Done!')
