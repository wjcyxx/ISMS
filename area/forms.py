from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class AreaModelForm(ModelForm):

    class Meta:
        model = area
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPosition': Fwidgets.Input(attrs={'class': 'layui-input',  'autocomplete': 'off'}),
            'FIsCheckworkatten': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '0'}),

        }

