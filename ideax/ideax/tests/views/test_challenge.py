from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http.response import Http404

from pytest import raises

from ...views import (challenge_detail, challenge_edit, challenge_remove)


class TestChallengeDetail:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = challenge_detail(request, 999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')


class TestChallengeEdit:
    def test_anonymous(self, rf):
        request = rf.get(f'/challenge/99999/edit/')
        request.user = AnonymousUser()
        response = challenge_edit(request, 99999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/challenge/99999/edit/')

    def test_not_found(self, rf, admin_user):
        request = rf.get(f'/challenge/99999/edit/')
        request.user = admin_user
        with raises(Http404):
            challenge_edit(request, 99999)

    def test_get_common_user(self, rf, common_user):
        request = rf.get('/challenge/1/edit/')
        request.user = common_user
        with raises(PermissionDenied):
            challenge_edit(request, 1)


class TestChallengeRemove:
    def test_anonymous(self, rf):
        request = rf.get('/')
        request.user = AnonymousUser()
        response = challenge_remove(request, 999)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/')

    def test_common_user(self, rf, common_user):
        request = rf.get('/')
        request.user = common_user
        with raises(PermissionDenied):
            challenge_remove(request, 1)

    def test_get(self, rf, mocker, messages):
        get_featured_challenges = mocker.patch('ideax.ideax.views.get_featured_challenges')
        get_featured_challenges.return_value = {}
        mocker.patch('ideax.ideax.views.Challenge')

        request = rf.get('/')
        request.user = mocker.Mock()
        request._messages = messages
        challenge_remove(request, 999)

        assert messages.is_success
        assert messages.messages == ['Challenge removed successfully!']
