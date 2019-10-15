from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class PedPassageModelForm(ModelForm):
    FDevID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FAreaID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = pedpassage
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPassage': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FType': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FInitStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '已初始化|未初始化', 'disabled': 'disabled'})
        }