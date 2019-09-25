from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class MaterialsModelForm(ModelForm):

    FGoodsTypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FUnitID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)


    class Meta:
        model = materials
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FMaterID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FName': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FSpec': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FTexture': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPositiveDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FNegativeDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FRFID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})

        }