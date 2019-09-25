from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class ProjectMapModelForm(ModelForm):
    FFilepath = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'layui-input', 'style': 'display: none'}))
    FMaptypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = projectmap
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FMapdesc': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
        }