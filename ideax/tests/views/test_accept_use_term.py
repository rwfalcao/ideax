from django.contrib.auth.models import AnonymousUser

from ...views import accept_use_term


class TestAcceptUseTermView:
    def test_accept_use_term_anonymous(self, rf):
        request = rf.get('/term/accept')
        request.user = AnonymousUser()
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/accounts/login/?next=/term/accept')

    def test_accept_use_term_not_accepted(self, ideax_views, rf, admin_user, messages, get_ip, mocker):
        ideax_views.audit = mocker.Mock()
        admin_user.userprofile.use_term_accept = False
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso aceito!']
        get_ip.assert_called_once_with(request)

    def test_accept_use_term_accepted(self, ideax_views, rf, admin_user, messages, mocker):
        ideax_views.audit = mocker.Mock()
        admin_user.userprofile.use_term_accept = True
        request = rf.get('/term/accept')
        request.user = admin_user
        request._messages = messages
        response = accept_use_term(request)
        assert (response.status_code, response.url) == (302, '/')
        assert messages.messages == ['Termo de uso já aceito!']
