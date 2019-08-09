from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from receaccount.models import *

class RecePoundModelForm(ModelForm):

    CREATED_PRJ = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FOperationalOrgID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FWorktypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = materialsaccount
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPoundNo': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FStatus': Fwidgets.Select(attrs={'lay-verify': 'required', 'disabled': 'disabled'}),
            'F1stWeighTime': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'F2ndWeighTime': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'F1stWeigh': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'F2ndWeigh': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FWeighPerson': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),
            'FPlate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FWarehouseID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FUsesite': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),

        }

class RecePoundMaterModelForm(ModelForm):

    FMaterID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'lay-filter': 'selMater'}), required=False)
    FUnitID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = materaccountgoods
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FWaybillQty': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FConfirmQty': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDeviationQty': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off', 'readonly': 'true'}),

        }