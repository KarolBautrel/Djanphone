from django.forms import  ModelForm, EmailField, EmailInput, ValidationError, ModelChoiceField,TextInput, CheckboxSelectMultiple
from .models import Product, User, Comment, Order, Store, Ticket,Contact,Message
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class EmailChangeForm(ModelForm):
    email2 = EmailField(label=('New email confirmation'), widget=EmailInput)
    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        cleaned_data = super().clean()
        new_email = cleaned_data.get('email')
        print(new_email)
        new_email2 = cleaned_data.get('email2')
        print(new_email2)
        email_db = User.objects.filter(email=new_email)
        if new_email != new_email2 or email_db:
            raise ValidationError ("Not valid email")
        else:
            print("Dupa")


class CheckoutShippingForm(forms.Form):
    shipping_city = forms.CharField( required = True)
    shipping_address = forms.CharField(required = True)
    shipping_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-control'
    }), required = False)
    shipping_zip = forms.CharField(required = True)
    
    same_billing_address = forms.BooleanField(required = False)

class CheckoutBillingForm(forms.Form):
    billing_city = forms.CharField( required = True)
    billing_address = forms.CharField(required = True)
    billing_country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-control'
    }), required = False)
    billing_zip = forms.CharField(required = True)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand','title','image','description','price']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body','user','product']


class TicketForm(ModelForm):
    
    body = forms.CharField(widget =  forms.Textarea(attrs={
        'placeholder': 'How can we help ? '}), required=True)
    subject = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Subject'}), required=True)
    class Meta:
        model = Ticket
        fields = ['body','subject']


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['products']   
        widgets = {
            'products' : CheckboxSelectMultiple
        }


#ADD VALIDATIONS
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['is_readed']

class CouponForm(forms.Form):
    code = forms.CharField(widget = TextInput(attrs = {
        'class': 'form-control',
        'placeholder':'Promo Code'
    }))
