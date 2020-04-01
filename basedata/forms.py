from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import base

class BasetypeModelForm(ModelForm):
    class Meta:
        model = base
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FBaseID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FBase': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMappingCode': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'})
        }

class BasedataModelForm(ModelForm):
    FPID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))

    class Meta:
        model = base
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FBaseID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FBase': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMappingCode': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
        }

