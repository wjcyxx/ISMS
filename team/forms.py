from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class TeamModelForm(ModelForm):
    FOrgID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = team
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FTeammgr': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMgrtel': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIDcard': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FFirstDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FScope': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FAmount': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FScale': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FEvaluate': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FSource': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '0'}),
        }