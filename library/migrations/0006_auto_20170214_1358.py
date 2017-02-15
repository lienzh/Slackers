# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 05:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20170214_1348'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='ISBN',
        ),
        migrations.AddField(
            model_name='book',
            name='info',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='library.BookInfo'),
            preserve_default=False,
        ),
    ]