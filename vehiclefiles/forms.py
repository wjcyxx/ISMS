from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class VehicleFilesModelForm(ModelForm):
    FOrgID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FVehicletypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FDevID = forms.ChoiceField(required=False)

    class Meta:
        model = vehiclefiles
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPlate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDrivers': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FValiddate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FRfidcard': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FIsMonitor': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '监控|不监控'}),
            'FTare': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})

        }