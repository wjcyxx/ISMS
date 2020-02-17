from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class PrjProcessModelForm(ModelForm):
    class Meta:
        model = prjprocess
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FProcessName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FScheduleTime': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FCompleteTime': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPlanStatus': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }