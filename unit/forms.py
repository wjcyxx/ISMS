from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class UnitModelForm(ModelForm):

    FUnitgroupID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = unit
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FUnit': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FConversion': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIsBaseunit': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
        }