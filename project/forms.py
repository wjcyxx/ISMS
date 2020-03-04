from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class ProjectModelForm(ModelForm):
    FPrjtypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))
    FPrjuseID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))
    FPrjstate = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))
    FStructypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))
    FManageORG = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}))

    class Meta:
        model = project
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPrjID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPrjname': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FShortname': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPrjcost': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FArea': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FAddress': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FLong': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLat': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSigDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSigbeginDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBeginDate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPrjmanager': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FPrjmanagertel': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FWinOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FWinAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FWinAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FConstrOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FConstrAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FConstrAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBuildOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBuildAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FBuildAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesignOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesignAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FDesignAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSuperviseOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSuperviseAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FSuperviseAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FUserOrgID': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FUserAtten': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FUserAttenTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FPrjdesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '0'}),
        }

