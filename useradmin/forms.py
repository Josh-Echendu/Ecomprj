from django import forms
from core.models import Product, Category


class ProductForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter product title', 'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Product Description', 'class': 'form-control'}))
    price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Sales Price', 'class': 'form-control'}))
    old_price = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'Old Price', 'class': 'form-control'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type of product e.g organic cream', 'class': 'form-control'}))
    stock_count = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'How many are in stock', 'class': 'form-control'}))
    life = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'How long will the product last', 'class': 'form-control'}))
    mfd = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tags (comma-separated)', 'class': 'form-control'}),required=False)

    # This two are optional
    digital = forms.BooleanField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['title', 'image', 'description', 'price', 'old_price', 'specifications', 'type', 'stock_count', 'life', 'mfd', 'tags', 'digital', 'category']
    
    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     tags_input = self.cleaned_data.get('tags', '')
    #     if tags_input:
    #         instance.tags.set(*[tag.strip() for tag in tags_input.split(',')])
    #     if commit:
    #         instance.save()
    #     return instance