from django import forms
from .models import Business

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['business_name', 'description', 'category', 'website', 'phone',
                  'address', 'city', 'state', 'country', 'zip_code',
                  'facebook_url', 'twitter_url', 'instagram_url',
                  'logo', 'founded_date', 'size', 'operating_hours', 'tax_id']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
            'operating_hours': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control mb-2'})
        
        # Customizing placeholders and other attributes
        self.fields['business_name'].widget.attrs.update({'placeholder': 'Enter your business name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Describe your business'})
        self.fields['website'].widget.attrs.update({'placeholder': 'https://www.example.com'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'e.g., +1 123-456-7890'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Street address'})
        self.fields['state'].widget.attrs.update({'placeholder': 'Region/State'})
        self.fields['city'].widget.attrs.update({'placeholder': 'City'})
        self.fields['country'].widget.attrs.update({'placeholder': 'Country'})
        self.fields['zip_code'].widget.attrs.update({'placeholder': 'Postal/Zip Code'})
        self.fields['facebook_url'].widget.attrs.update({'placeholder': 'https://www.facebook.com/yourbusiness'})
        self.fields['twitter_url'].widget.attrs.update({'placeholder': 'https://www.twitter.com/yourbusiness'})
        self.fields['instagram_url'].widget.attrs.update({'placeholder': 'https://www.instagram.com/yourbusiness'})
        self.fields['tax_id'].widget.attrs.update({'placeholder': 'Your business tax ID'})
        self.fields['operating_hours'].widget.attrs.update({'placeholder': 'e.g., Mon-Fri: 9AM-5PM, Sat: 10AM-3PM, Sun: Closed'})

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Basic phone number validation
            if not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean_tax_id(self):
        tax_id = self.cleaned_data.get('tax_id')
        if tax_id:
            # Basic tax ID validation (you may want to customize this based on your country's format)
            if not tax_id.isalnum() or len(tax_id) < 8:
                raise forms.ValidationError("Please enter a valid tax ID.")
        return tax_id

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if logo:
            # Limit logo file size (e.g., to 5MB)
            if logo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 5MB )")
        return logo
    



class BusinessUpdateForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ['user']  # We don't want to allow changing the user associated with the business
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_date': forms.DateInput(attrs={'type': 'date'}),
            'operating_hours': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})







