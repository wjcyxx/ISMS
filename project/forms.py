from django.forms import ModelForm
from django import forms
from django.forms import widgets as Fwidgets
from .models import *

class ProjectModelForm(ModelForm):

    class Meta:
        model = project
        fields = '__all__'


