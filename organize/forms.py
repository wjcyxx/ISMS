from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class OrganizeModelForm(ModelForm):

    class Meta:
        model = organize
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FQualevel': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FOrgname': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
        }
