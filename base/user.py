
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import (
                    User,
                     MessageReceiver,
                     Message
                    )
from .forms import EmailChangeForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (UpdateView,
                                ListView,
                                DetailView,
                                )
from django.contrib.auth.mixins import LoginRequiredMixin

class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'base/profile.html'


class UpdateUserView(UpdateView, LoginRequiredMixin):
    model = User
    fields = ['name', 'country', 'city']
    template_name  = 'base/update_profile.html'
    
    def get_form(self, form_class=None):
        form = super(UpdateUserView, self).get_form(form_class)
        form.fields['name'].required = True
        form.fields['country'].required = True
        form.fields['city'].required = True
        return form

def settingsPanel(request):
    return render(request, 'base/account_setting.html')


def changePassword(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Change completed')
            return redirect('home')
        else:
            messages.error(request, 'Old password incorrect or new passwords doesnt match')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'base/change_password.html', context)


def changeEmail(request):
    user = request.user
    if request.method == 'POST':
        form = EmailChangeForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Change completed')
            return redirect('home')
        else:
             messages.error(request, 'Invalid email')
    else:
        request.method == 'GET'
        form = EmailChangeForm(instance = user) 
    context={'form':form}
    return render(request, 'base/change_email.html', context)


class InboxView( ListView):
    model = MessageReceiver
    context_object_name = 'notifications'
    paginate_by = 5
    template_name = 'base/inbox.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset() 
        queryset = qs.filter(receiver = self.request.user)
        return queryset


class MessageDetailView( DetailView):
    model = MessageReceiver
    context_object_name = 'message'
    template_name = 'base/message_detail.html'
    

# TODO: support
@login_required
def read_message(request, pk):
    message = MessageReceiver.objects.get(id=pk)
    message.is_readed = True
    message.save()
    return redirect('inbox')


@login_required
def delete_message(request, pk):
    message = MessageReceiver.objects.get(id=pk)
    message.delete()
    messages.success(request, f'Message has been deleted')
    return redirect('inbox')