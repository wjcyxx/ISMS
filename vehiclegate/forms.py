from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class VehicleGateModelForm(ModelForm):
    FDevID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FAreaID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = vehiclegate
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FGate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FGatetype': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FGateattr': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }

class VehicleSiginModelForm(ModelForm):
    FVehtypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = vehiclesigin
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FIsCurrent': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '允许通行|禁止通行'}),
            'FIsIndefinite': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否'}),
            'FBegindate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FEnddate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }