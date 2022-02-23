from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from .models import (
                    User,
                    Ticket,
                    Contact,
                    )
from .forms import TicketForm

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect

from django.views.generic import (
                                CreateView,
                                )
from django.urls import reverse


class TicketCreationView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name  = 'base/ticket.html'
    redirect_field_name = 'base/login.html'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.ticket_creator = self.request.user
        obj.save()        
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('ticket-panel', kwargs = {'pk': self.request.user.id})


class ContactView(CreateView):
    model = Contact
    fields = '__all__'
    template_name  = 'base/contact.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        send_mail(
            'Thank you for contact',
            f'Our team is reviewing your message, stay tuned for answer(your message {obj.body[0:20]})',
            'testbautrel111@gmail.com',
            [f'{obj.email}'],
            )
        messages.success(self.request, 'Our team is reviewing your message')
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('home')

def ticketConfirmation(request):
    return render(request, 'base/ticket_confirm.html')


@login_required
def ticketPanel (request, pk):
    user = User.objects.get(id=pk)
    tickets = user.ticket_set.all()
    context = {'user':user, 'tickets':tickets}
    return render(request,'base/tickets.html', context)


def ticketInfo(request,pk):
    ticket = Ticket.objects.get(id=pk)
    context= {'ticket':ticket}
    return render(request, 'base/ticket_info.html', context)
