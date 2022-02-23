
from django.shortcuts import render, redirect, get_object_or_404
from .models import (Product,
                    User,
                    Message,
                    MessageReceiver
                    )               
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse

def adminPanel(request):
    return render(request, 'base/superuser_panel.html')


class ProductCreateView(CreateView):
    model = Product
    fields = ['title','brand','price','image','description']
    template_name = 'base/product_create.html'


class SendMessageCreationView(PermissionRequiredMixin,CreateView):
        permission_required = 'is_staff'
        model = Message
        context_object_name = 'message'
        fields =['subject','body']
        template_name = 'base/message.html'
        redirect_field_name = 'base/login.html'

        def get_form(self, form_class=None):
            form = super(SendMessageCreationView, self).get_form(form_class)
            form.fields['subject'].required = True
            form.fields['body'].required = True
            return form


    # TODO CONFIGURE MASS SENDING
        def form_valid(self, form):
            obj = form.save(commit=False)
            obj.creator = self.request.user
            obj.save()
            receiver = User.objects.all()
            for man in receiver:
                if man.is_superuser == False:
                    MessageReceiver.objects.create(
                        message = obj,
                        is_readed = False,
                        receiver = man
                        )
            messages.success(self.request, f'Message has been sent')
            return HttpResponseRedirect(self.get_success_url())
            
        def get_success_url(self):
            return reverse('home')