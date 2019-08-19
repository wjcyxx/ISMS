from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class MonitorDevModelForm(ModelForm):
    FAreaID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = monitordev
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FChannel': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIPAddress': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FAccessuser': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FAccesspwd': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDevtype': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FIsYuntai': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否'}),
            'FChannelNo': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPort': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FProtocoltype': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FProtocol': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FTransmode': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FIsOpenAudio': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '开启|关闭'}),
            'FIsOpenVideo': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '开启|关闭'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})

        }