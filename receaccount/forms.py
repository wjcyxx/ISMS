from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class ReceAccountModelForm(ModelForm):

    CREATED_PRJ = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}), required=False)
    FOperationalOrgID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}), required=False)
    FWorktypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}), required=False)

    class Meta:
        model = materialsaccount
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPoundNo': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FStatus': Fwidgets.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}),
            'F1stWeighTime': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'F2ndWeighTime': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'F1stWeigh': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'F2ndWeigh': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FWeighPerson': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FPlate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FWarehouseID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FUsesite': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1', 'readonly': 'true'}),



        }