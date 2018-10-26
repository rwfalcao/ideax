from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from .forms import SignUpForm


@login_required
def profile(request):
    return render(
        request,
        'users/profile.html',
        {
            'user': request.user,
            'ideas': request.user.userprofile.authors.all(),
        }
    )


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('index')
    template_name = 'users/sign_up.html'

    def form_invalid(self, form):
        messages.error(self.request, _('Invalid form!'))
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return response
