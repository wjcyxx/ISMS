from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class MencRepairLogModelForm(ModelForm):
    FSubmitter = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = mencrepairlog
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FSubmitdate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FHappendate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FSite': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})

        }