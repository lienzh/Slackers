#!/usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Lestock.settings") 

import django
django.setup()

def main():
	from stock.models import Inventory,Device
	f = open('deviceData.txt')
	for line in f:
		ERP,description,quota,quotanum,unit,price,devimg,devclass,usesys,usepart = line.split('\'')
		#ERP, description, location, quantity = line.split('')
		Device.objects.get_or_create(ERP=ERP, description=description, quota=quota, quotanum=quotanum, unit=unit, price=price, devimg=devimg, devclass=devclass, usesys=usesys, usepart=usepart)
	f.close()

if __name__ == "__main__":
	main()
	print('Done!')
