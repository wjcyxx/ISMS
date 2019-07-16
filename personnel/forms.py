from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class PersonModelForm(ModelForm):
    FTeamID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FGroupID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)
    FWorktypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required', 'lay-filter': 'selworktype'}), required=False)

    class Meta:
        model = personnel
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FGroup': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FType': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FIsSafetrain': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否', 'disabled': 'disabled'}),
            'FSpecialequ': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否', 'disabled': 'disabled'}),
            'FSafetrainDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSafetrainHour': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FIDcard': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIDcardbeginDate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIDcardendDate': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FIDcardIsIndefinite': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '是|否', 'disabled': 'disabled'}),
            'FSex': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FNation': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBirthday': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FNaviveplace': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FHomeaddress': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSignorg': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPolitident': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSpeciality': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMarital': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FLevelofedu': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FTempaddress': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBank': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBankaccount': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FEmercontact': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FEmercontacttel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
        }