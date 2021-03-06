from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class OrganizeModelForm(ModelForm):
    FOrgtypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = organize
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FQualevel': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FOrgname': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FOrgaddress': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FLat': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLong': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLar': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FLartel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLarIDcard': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FRegcapital': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FRegDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLicenceno': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FValidDate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FLicauthority': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FHrcharge': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FHrIDcard': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FHrtel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FIssplit': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '???|???'}),
            'FStatus': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FScope': Fwidgets.Textarea(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        super(OrganizeModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': '*'}


class OrganizeQualiModeForm(ModelForm):
    FFilepath = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'layui-input', 'style': 'display: none'}))

    class Meta:
        model = orgQualifications
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FQualification': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FFilename': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
        }