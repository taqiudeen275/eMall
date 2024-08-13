from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'billing_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    use_different_billing_address = forms.BooleanField(required=False, initial=False,
                                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['billing_address'].required = False

    def clean(self):
        cleaned_data = super().clean()
        use_different_billing_address = cleaned_data.get('use_different_billing_address')
        billing_address = cleaned_data.get('billing_address')

        if not use_different_billing_address:
            cleaned_data['billing_address'] = cleaned_data.get('shipping_address')
        elif use_different_billing_address and not billing_address:
            self.add_error('billing_address', 'Please provide a billing address.')

        return cleaned_data