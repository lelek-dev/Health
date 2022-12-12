from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import HealthUser

class HealthUserCreationForm(UserCreationForm):
    class Meta:
        model = HealthUser
        fields = ("username", "email")
    dataprivacy = forms.BooleanField(label="I accept to the Privacy Policy.", required = True)
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(HealthUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():      
            if visible.name == "dataprivacy":
                visible.field.widget.attrs['class'] = 'form-check-control'
            else:
                visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'

class HealthUserChangeForm(UserChangeForm):
    class Meta:
        model = HealthUser
        fields = ("username", "email")

class HealthUserUpdateForm(UserChangeForm):
    class Meta:
        model = HealthUser
        fields = ("username", "email")
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(HealthUserUpdateForm, self).__init__(*args, **kwargs)
        del self.fields['password']
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'

class HealthUserForm(forms.ModelForm):
    class Meta:
        model=HealthUser
        fields=('username','email')
    template_name = "form_snippet.html"
    def __init__(self, *args, **kwargs):
        super(HealthUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'