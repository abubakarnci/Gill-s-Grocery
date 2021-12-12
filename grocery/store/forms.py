from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

# creating forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', 'email', 'password1', 'password2']
        
        
class CustomerForm(ModelForm):
    class Meta:
        model= Customer
        fields = '__all__'
        exclude = ['user']
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model= Comment
        fields = ('commenter_body',)
        widgets = {
            'commenter_body': forms.Textarea(attrs={'class': 'form-control'}),
        }