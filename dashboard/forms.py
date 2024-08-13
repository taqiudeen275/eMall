from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image','url', 'position', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 3})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['url'].widget.attrs.update({'class': 'form-control'})
        self.fields['position'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})

