from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class GoosTypeModelForm(ModelForm):

    class Meta:
        model = goodstype
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FGoodsTypeID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FGoodsType': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDeviationType': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FPositiveDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FNegativeDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'})
        }

class SubTypeModelForm(ModelForm):

    FPID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}), required=False)

    class Meta:
        model = goodstype
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FGoodsTypeID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FGoodsType': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDeviationType': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FPositiveDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FNegativeDeviation': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'})
        }
