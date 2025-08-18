from django import forms
from .models import Restaurant 

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback 
        fields = ['comments']
        widgets = {
            'comments' : forms.Textarea(attrs={'rows':4, 'placeholder':"Your thots to Write Here....."}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
        }