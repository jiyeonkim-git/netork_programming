from django import forms
from .models import Contact

class MyForm(forms.Form):
    my_name = forms.CharField(label='Your name', max_length=100)

class NameForms(forms.Form):
    favorite_name = forms.CharField(label='Favorite Name', max_length=100)

class ContactForm(forms.Form):
    class Meta:
        model = Contact
        fields = ['subject', 'message', 'sender']
        # exclude = ['cc_myself']
        # fields = '__all__'