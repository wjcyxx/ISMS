from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class BusMenuModelForm(ModelForm):
    FPID = forms.ChoiceField(required=False)

    class Meta:
        model = busmenu
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FSequence': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMenuID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMenuName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FUrl': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMenuIcon': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMenuPosition': Fwidgets.Select(),
            'FFoldState': Fwidgets.Select(),
            'FFormState': Fwidgets.Select(),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),

        }

