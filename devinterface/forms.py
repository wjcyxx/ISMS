from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class DeviceInterfaceModelForm(ModelForm):
    FDevID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FInterfaceTypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = devinterface
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FTransmode': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FInterval': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FAddress': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
        }