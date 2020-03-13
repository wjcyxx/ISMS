from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class DeviceInterfaceModelForm(ModelForm):
    FAppFID = forms.ChoiceField(required=False)
    FDevID = forms.ChoiceField(required=False)   #已废弃
    FInterfaceTypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FInterfaceExtID = forms.ChoiceField(required=False)   #已废弃

    class Meta:
        model = devinterface
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FTransmode': Fwidgets.Select(),
            'FRequestType': Fwidgets.Select(),
            'FInterfaceAttribID': Fwidgets.Select(),
            'FInterval': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FAddress': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPort': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSrvFile': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FScope': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FCallSigCode': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FSrvStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '运行|停止', 'disabled': 'disabled'}),

        }


class InterfaceParamModelForm(ModelForm):
    FTypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = interfaceparam
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FSequence': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPosition': Fwidgets.Select(),
            'FParam': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FValue': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),

        }


class SubInterfaceModelForm(ModelForm):
    FInterfaceID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = subinterface
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),

            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
        }