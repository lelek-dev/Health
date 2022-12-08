from django import forms
from .models import HealthRecordFolder, HealthRecord
from django.core import validators

class HealthRecordFolderForm(forms.ModelForm):
    class Meta:
        model=HealthRecordFolder
        fields=('title','description')
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(HealthRecordFolderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model=HealthRecord
        fields=('title','description', 'media')
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(HealthRecordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'

class ShareHealthRecordForm(forms.Form):
    doctor = forms.ChoiceField(label="Doctor", validators=[validators.validate_integer])
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(ShareHealthRecordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'

