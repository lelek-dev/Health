from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import logout
from .forms import HealthUserCreationForm, HealthUserUpdateForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import HealthUser
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from doctor.views import send_400

class SignUpView(CreateView):
    form_class = HealthUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def UpdateView(request):
    if request.method == 'POST':
        form = HealthUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('internalAuth:update'))
    else:
        form = HealthUserUpdateForm(instance=request.user)
    return render(request, 'profile/update.html', {'form': form})

def DeleteView(request):
    user = get_object_or_404(HealthUser, pk=request.user.pk)
    user.delete()
    logout(request)
    return HttpResponseRedirect('/')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset/password_reset.html'
    email_template_name = 'password_reset/password_reset_email.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')