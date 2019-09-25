from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *
from receaccount.models import *

class AbnPoundModelForm(ModelForm):

    class Meta:
        model = abnpound
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPoundID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FResult': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FResultDate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }