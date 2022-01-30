from django.forms import  ModelForm, EmailField, EmailInput, ValidationError, ModelChoiceField, CheckboxSelectMultiple
from .models import Product, User, Comment, Shipment, Ticket, Delivery, Store

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

   

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['brand','model','name','image','description','price']




class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']



class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'


class BudgetForm(ModelForm):
    class Meta:
        model = User
        fields = ['budget']


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['body', 'shipment']
        

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields['shipment'] = ModelChoiceField(queryset=user.shipment_set.all())

    

class DeliveryForm(ModelForm):
    class Meta:
        model = Delivery
        fields = '__all__'


class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['products']   
        widgets = {
            'products' : CheckboxSelectMultiple

        }

