from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from login.models import User

class UserModelForm(ModelForm):
    FOrgID = forms.ChoiceField(required=False)
    FRoleID = forms.ChoiceField(required=False)

    class Meta:
        model = User
        fields = "__all__"

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FUserID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FUserpwd': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FType': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FUsername': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FTel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
        }
