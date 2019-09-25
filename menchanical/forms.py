from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class MenchModelForm(ModelForm):
    FMonitordevID = forms.ChoiceField(required=False)
    FMectypeID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = menchanical
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FMecserialID': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMecspec': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FMecsource': Fwidgets.Select(attrs={'lay-verify': 'required'}),
            'FOwnerOrg': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FRecordNo': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FRecorddate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FLease': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FManufacturer': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FProducdate': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FProducNo': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMecmanager': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FMecmanagertel': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FParameter': Fwidgets.Input(attrs={'class': 'layui-input', 'autocomplete': 'off'}),
            'FStatus': Fwidgets.CheckboxInput(attrs={'lay-skin': 'switch', 'lay-text': '启用|禁用', 'disabled': 'disabled'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }

class MecOperAuthModelForm(ModelForm):
    FAuthpersonID = forms.ChoiceField(widget=forms.Select(attrs={'lay-verify': 'required'}), required=False)

    class Meta:
        model = mecoperauth
        fields = '__all__'

        widgets = {
            'FID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FPID': Fwidgets.Input(attrs={'type': 'hidden'}),
            'FAuthTimeslot': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FAuthDeadline': Fwidgets.Input(attrs={'class': 'layui-input', 'lay-verify': 'required', 'autocomplete': 'off'}),
            'FDesc': Fwidgets.Textarea(attrs={'class': 'layui-textarea', 'autocomplete': 'off', 'rows': '1'})
        }