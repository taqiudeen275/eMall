from django import forms
from .models import Product, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    primary_image = forms.ImageField(required=True)
    additional_images = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def clean_additional_images(self):
        """
        Handle multiple file uploads.
        """
        files = self.files.getlist('additional_images')
        if len(files) > 5:  # Example: limit to 5 additional images
            raise forms.ValidationError("You can upload a maximum of 5 additional images.")
        return files

    def save(self, commit=True):
        product = super().save(commit=False)
        if commit:
            product.save()
            if self.cleaned_data.get('primary_image'):
                ProductImage.objects.create(product=product, image=self.cleaned_data['primary_image'], is_primary=True)
            for image in self.cleaned_data.get('additional_images', []):
                ProductImage.objects.create(product=product, image=image)
        return product
    

from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
