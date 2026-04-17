from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductFilter(forms.Form):
    query = forms.CharField(
        required=False,
        label='Поиск',
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по имени'}) 
    )
    sort = forms.ChoiceField( 
        required=False,
        label='Сортировка',
        choices=[ 
            ('', 'Без сортировки'),
            ('final_price', 'Сортировка вверх'),
            ('-final_price', 'Сортировка вниз')
        ]
    )