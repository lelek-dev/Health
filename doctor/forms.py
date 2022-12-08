from django import forms

class ShareHealthRecordForm(forms.Form):
    accept_invite = forms.BooleanField(label="Accept Invite")
    template_name = "checkbox_snippet.html"
    def __init__(self, *args, **kwargs):
        super(ShareHealthRecordForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-check-control'
            visible.field.widget.attrs['placeholder'] = 'hopefully not visible'
