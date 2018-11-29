from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView
from django.db.models import Count, Case, When

from .forms import SignUpForm
from ..ideax.models import Popular_Vote, Comment, Idea
from .models import UserProfile


@login_required
def profile(request, pk):
    if pk == 0:
        votes = Popular_Vote.objects.filter(voter=request.user.id).values(
            'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=request.user.id).values('raw_comment')
        return render(
            request,
            'users/profile.html',
            {
                'user': request.user,
                'ideas': request.user.userprofile.authors.all(),
                'popular_vote': votes[0]['contador'],
                'comments': len(comments),
            }
        )
    else:
        votes = Popular_Vote.objects.filter(voter=pk).values(
            'voter_id').annotate(contador=Count(Case(When(like=True, then=1))))
        comments = Comment.objects.filter(author_id=pk).values('raw_comment')
        if not votes:
            getvotes = 0
        else:
            getvotes = votes[0]['contador']
        return render(
            request,
            'users/profile.html',
            {
                'user': UserProfile.objects.filter(id=pk)[0].user,
                'ideas': UserProfile.objects.filter(id=pk)[0].user.userprofile.authors.all(),
                'popular_vote': getvotes,
                'comments': len(comments),
            }
        )


@login_required
def who_innovates(request):
    data = dict()
    data['ideas'] = Idea.objects.values("author__user__username", "author__user__email", "author_id").annotate(
        qtd=Count('author_id')).annotate(
        count_dislike=Count(Case(When(popular_vote__like=False, then=1)))).annotate(
        count_like=Count(Case(When(popular_vote__like=True, then=1))))

    return render(request, 'users/who_innovates.html', data)


class SignUpView(CreateView):
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
