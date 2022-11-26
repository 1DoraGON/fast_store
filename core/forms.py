from random import choices
from django import forms
from django.http import HttpRequest
from core.constants import CIB, DELIVERY_MODE, EDAHABIA, WILAYA

PAYMENT_MODE = {
    (CIB, "CIB"),
    (EDAHABIA, "EDAHABIA"),
}


class CheckoutForm(forms.Form):
    receiver_firstname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder':'Receiver Firstname'
    }))
    receiver_lastname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder':'Receiver Lastname'
    }))
    wilaya = forms.ChoiceField(choices= WILAYA)
    address1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder':'address 1'
    }))
    address2 = forms.CharField(max_length=200,required=False,widget=forms.TextInput(attrs={
        'placeholder':'address 2'
    }))
    apartment_address = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder':'apartment or suite'
    }))
    zip = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder':'xxxxx'
    }))
    phone = forms.CharField(max_length=10, widget=forms.NumberInput(attrs={
        'placeholder':"Please don't mistake"
    }))
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_MODE)
    delivery_mode = forms.ChoiceField(
        widget=forms.RadioSelect, choices=DELIVERY_MODE)
