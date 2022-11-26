from django import forms
from core.constants import SUPERVISOR_TYPE,LABEL_CHOICES
from core.models import Category
from django.core.files.storage import FileSystemStorage

class SupervisorForm(forms.Form):
    email = forms.EmailField(max_length=70, widget=forms.EmailInput(attrs={
        "placeholder":"Email must be for an existing account",
        "class":"form-control"
    }))
    supervisor_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=SUPERVISOR_TYPE)

class CategoryForm(forms.Form):
    category_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Category name (Jeans,Chemise ...)"
    }))

class ItemForm(forms.Form):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Item title"
    }))
    label = forms.ChoiceField(widget=forms.RadioSelect(attrs={
        "class":"form-check-input",
        "type":"radio"
    }), choices=LABEL_CHOICES)
    price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "class":"form-control",
        "placeholder":"Item price"
    }))
    discount_price = forms.DecimalField(widget=forms.NumberInput(attrs={
        "class":"form-control",
        "placeholder":"Item discount, default is 0"
    }))
    category = forms.ModelChoiceField(queryset = Category.objects.all(), widget=forms.Select(attrs={
        "class":"form-control"
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        "class":"form-control",
        "id":"exampleFormControlTextarea1",
        "rows":"3",
        "placeholder":"Item available sizes, colors and other infos"
    }))
    quantity = forms.CharField(widget=forms.NumberInput(attrs={
        "class":"form-control",
        "placeholder":"Item quantity, if you dont want to specify quantity leave it blank"
    }))