from django import forms
from django.forms import Form, ModelForm

from .models import Activity, ActivityType


class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = []


class ImportGPXFileForm(Form):
    activity_type = forms.ChoiceField(choices=ActivityType.objects.all().values_list('id', 'name'))
    gpx_file = forms.FileField()
