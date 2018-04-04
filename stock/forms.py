#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

class SearchForm(forms.Form):
        CHOICES = [
            (u'ERP', u'ERP'),
            (u'描述', u'描述'),
            (u'使用方向', u'使用方向')
        ]

        search_by = forms.ChoiceField(
            label='',
            choices=CHOICES,
            widget=forms.RadioSelect(),
            initial=u'描述',
        )

        keyword = forms.CharField(
            label='',
            max_length=32,
            widget=forms.TextInput(attrs={
                'class': 'form-control input-lg',
                'placeholder': u'请输入需要检索的备件信息',
                'name': 'keyword',
            })
        )


class UploadFileForm(forms.Form):
	title = forms.CharField(max_length=50)
	file  = forms.FileField()

