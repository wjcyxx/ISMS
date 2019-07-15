from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class GroupModelForm(ModelForm):
    FTeamID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FWorktypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'lay-filter': 'selworktype'}), required=False)

    class Meta:
        model = group
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FGroup': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
        }