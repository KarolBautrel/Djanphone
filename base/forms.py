from django.forms import  ModelForm, EmailField, EmailInput, ValidationError
from .models import Product, User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'bio','avatar']