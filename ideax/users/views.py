from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _

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


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, _('Invalid form!'))
    else:
        form = SignUpForm()
    return render(request, 'users/sign_up.html', {'form': form})
