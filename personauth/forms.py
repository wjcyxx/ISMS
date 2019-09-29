from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class PersonAuthModelForm(ModelForm):
    FAuthtypeID = forms.ChoiceField(widget=forms.Select(attrs={'disabled': 'disabled'}), required=False)

    class Meta:
        model = personauthmode
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FFeaturevalue': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FAuthvalidity': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FAuthtimequm': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FStatus': Fwidgets.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}),
        }