from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class DeviceModelForm(ModelForm):
    FDevtypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = device
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FDevID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDevice': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDevIP': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPort': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FManufacturer': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBrand': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMainstaff': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMainstafftel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FWarrantyDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
        }