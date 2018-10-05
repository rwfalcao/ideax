from pytest import fixture
from django.contrib.auth.models import AnonymousUser

from ideax.views import accept_use_term


class TestViews:
    @fixture
    def get_ip(self, mocker):
        patch = mocker.patch('ideax.views.get_ip')
        patch.return_value = '1.1.1.1'
        return patch

    def test_accept_use_term_anonymous(self, rf):
        request = rf.get('/term/accept')
        request.user = AnonymousUser()
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/term/accept')

    def test_accept_use_term_not_accepted(self, rf, admin_user, messages, get_ip):
        admin_user.userprofile.use_term_accept = False
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso aceito!']
        get_ip.assert_called_once_with(request)

    def test_accept_use_term_accepted(self, rf, admin_user, messages):
        admin_user.userprofile.use_term_accept = True
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso já aceito!']
