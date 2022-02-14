from django.forms import  ModelForm, EmailField, EmailInput, ValidationError, ModelChoiceField, CheckboxSelectMultiple
from .models import Product, User, Comment, Order, Store, Ticket,Contact,Message
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
PAYMENT_CHOICES=(
    ('Paypal', 'Paypal'), 
    ('Stripe','Stripe'), 
    ('PayU','PayU')
)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'bio','avatar','address']


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


class CheckoutForm(forms.Form):
    street_address = forms.CharField( widget = forms.TextInput(attrs={
                'placeholder':'Warsaw 1234',
                'class':'form-control'}))
    apartment_address = forms.CharField(widget = forms.TextInput(attrs={
                'placeholder':'Street or Home',
                'class':'form-control'}), required = False)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-control'
    }))
    zip = forms.CharField(widget= forms.TextInput(attrs={
        'class':'form-control'
    }))
    same_shipping_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand','title','image','description','price']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body','user','product']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user','delivery']


class BudgetForm(ModelForm):
    class Meta:
        model = User
        fields = ['budget']


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
        fields = ['subject','receiver','body']

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        sender = self.request.user
        receiver = self.cleaned_data['receiver']
        if sender == receiver:
            raise ValidationError ("You cant send message to yourself")