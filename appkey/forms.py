from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class AppKeyModelForm(ModelForm):
    class Meta:
        model = appkey
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FAppkey': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off', 'readonly': 'true'}),
            'FAppName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'})
        }